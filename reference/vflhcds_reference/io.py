"""Independent version-1 graph/set IO and exact reference result records."""

from fractions import Fraction
import hashlib
import json
import re

from .direct import Reference, SizeLimitError
from .graph import Graph, normalize_graph


class GraphFormatError(ValueError):
    pass


def decimal_text(value: int) -> str:
    try:
        return str(value)
    except ValueError as error:
        raise SizeLimitError("interpreter decimal-digit resource limit reached") from error


def decimal_integer(token: str, *, signed: bool = False) -> int:
    pattern = r"(?:0|-[1-9][0-9]*|[1-9][0-9]*)" if signed else r"(?:0|[1-9][0-9]*)"
    if not re.fullmatch(pattern, token):
        raise ValueError("expected canonical decimal integer")
    try:
        return int(token)
    except ValueError as error:
        # Python's configurable decimal-conversion limit is a resource limit,
        # not permission to truncate, round or relabel a large original ID.
        raise SizeLimitError("interpreter decimal-digit resource limit reached") from error


def parse_fraction(token: str) -> Fraction:
    parts = token.split("/")
    if len(parts) != 2:
        raise ValueError("lambda must be A/B")
    numerator, denominator = (decimal_integer(part) for part in parts)
    if denominator == 0:
        raise ValueError("lambda denominator must be positive")
    return Fraction(numerator, denominator)


class _Tokens:
    def __init__(self, text: str):
        try:
            text.encode("ascii")
        except UnicodeEncodeError as error:
            raise ValueError("canonical graph/set syntax must be ASCII") from error
        self.tokens = iter(text.split())

    def take(self, expected: str | None = None) -> str:
        token = next(self.tokens, None)
        if token is None or (expected is not None and token != expected):
            raise ValueError(f"missing or unexpected token; expected {expected or 'a value'}")
        return token

    def vertices(self) -> tuple[int, ...]:
        self.take("n")
        count = decimal_integer(self.take())
        result = []
        for _ in range(count):
            self.take("v")
            result.append(decimal_integer(self.take(), signed=True))
        return tuple(result)

    def finish(self):
        if next(self.tokens, None) is not None:
            raise ValueError("unexpected trailing records")


def parse_graph(text: str) -> Graph:
    try:
        tokens = _Tokens(text)
        tokens.take("vflhcds-graph")
        tokens.take("1")
        vertices = tokens.vertices()
        tokens.take("m")
        count = decimal_integer(tokens.take())
        edges = []
        for _ in range(count):
            tokens.take("e")
            edges.append((decimal_integer(tokens.take(), signed=True),
                          decimal_integer(tokens.take(), signed=True)))
        tokens.finish()
        normalized = normalize_graph(vertices, edges)
        if normalized.removed_self_loops or normalized.removed_duplicate_edges:
            raise ValueError("canonical input must not contain loops or duplicate edges")
        return normalized.graph
    except SizeLimitError:
        raise
    except ValueError as error:
        raise GraphFormatError(str(error)) from error


def parse_set(text: str, graph: Graph) -> int:
    tokens = _Tokens(text)
    tokens.take("vflhcds-set")
    tokens.take("1")
    vertices = tokens.vertices()
    tokens.finish()
    return graph.mask(vertices)


def canonical_graph(graph: Graph) -> str:
    lines = ["vflhcds-graph 1", f"n {graph.n}"]
    lines.extend("v " + decimal_text(v) for v in graph.vertices)
    lines.append(f"m {len(graph.edges)}")
    lines.extend("e " + decimal_text(u) + " " + decimal_text(v) for u, v in graph.edges)
    return "\n".join(lines) + "\n"


def graph_sha256(graph: Graph) -> str:
    return hashlib.sha256(canonical_graph(graph).encode("ascii")).hexdigest()


def fraction_record(value: Fraction) -> dict:
    return {"num": decimal_text(value.numerator), "den": decimal_text(value.denominator)}


def solution_records(ref: Reference, ranked: tuple[int, ...]) -> list[dict]:
    records = []
    for rank, mask in enumerate(ranked, start=1):
        density = ref.density(mask)
        records.append({"rank": rank, "h": ref.h, "vertex_count": mask.bit_count(),
                        "clique_count": decimal_text(ref.mu_h(mask)), "density_num": decimal_text(density.numerator),
                        "density_den": decimal_text(density.denominator), "vertices": list(ref.graph.ids(mask))})
    return records


def oracle_record(ref: Reference, result) -> dict:
    return {"scope": result.scope, "h": ref.h, "lambda_num": decimal_text(result.parameter.numerator),
            "lambda_den": decimal_text(result.parameter.denominator), "vertex_count": result.largest.bit_count(),
            "clique_count": decimal_text(ref.mu_h(result.largest)), "vertices": list(ref.graph.ids(result.largest))}


def json_line(value) -> str:
    try:
        return json.dumps(value, ensure_ascii=True, separators=(",", ":"), allow_nan=False) + "\n"
    except ValueError as error:
        raise SizeLimitError("JSON integer serialization resource limit reached") from error

"""Independent exponential reference CLI. Not the production vflhcds CLI."""

import argparse
import os
from pathlib import Path
import sys
import tempfile

from .direct import DEFAULT_MAX_VERTICES, Reference, SizeLimitError, direct_lhcds
from .io import (GraphFormatError, decimal_integer, decimal_text, fraction_record, graph_sha256, json_line,
                 oracle_record, parse_fraction, parse_graph, parse_set, solution_records)
from .parametric import cardinality_line_chain, exhaustive_F, exhaustive_restricted


class _Parser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError(message)


def _positive(token):
    value = decimal_integer(token)
    if value < 1:
        raise ValueError("value must be at least 1")
    return value


def _h(token):
    value = _positive(token)
    if value < 2:
        raise ValueError("h must be at least 2")
    return value


def _parser():
    parser = _Parser(description="Independent exact tiny-graph reference (default n<=12)", allow_abbrev=False)
    subparsers = parser.add_subparsers(dest="command", required=True, parser_class=_Parser)
    for name in ["truth", "oracle", "chain"]:
        command = subparsers.add_parser(name, allow_abbrev=False)
        command.add_argument("--graph", required=True)
        command.add_argument("--h", required=True, type=_h)
        command.add_argument("--max-vertices", type=_positive, default=DEFAULT_MAX_VERTICES)
        command.add_argument("--seed", type=decimal_integer, help="record fixture/generator seed only")
        command.add_argument("--output", default="-")
        if name == "truth":
            mode = command.add_mutually_exclusive_group(required=True)
            mode.add_argument("--k", type=_positive)
            mode.add_argument("--all", action="store_true")
        if name == "oracle":
            command.add_argument("--lambda", dest="parameter", type=parse_fraction, required=True)
            command.add_argument("--x")
            command.add_argument("--y")
    return parser


def _read(path: str) -> str:
    # Decode as UTF-8 here; syntax validation distinguishes malformed graphs from
    # set/request errors. Non-ASCII valid UTF-8 is rejected by the corresponding parser.
    return Path(path).read_text(encoding="utf-8")


def _write_output(path: str, text: str):
    if path == "-":
        sys.stdout.write(text)
        sys.stdout.flush()
        return
    target = Path(path)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n",
                                         dir=target.parent, prefix=target.name + ".", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(text)
            stream.flush()
        os.replace(temporary, target)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def _execute(args):
    if args.command == "oracle" and (args.x is None) != (args.y is None):
        raise ValueError("--x and --y must be supplied together")
    inputs = [args.graph]
    if args.command == "oracle" and args.x is not None:
        inputs.extend([args.x, args.y])
    if args.output != "-":
        target = Path(args.output)
        for name in inputs:
            source = Path(name)
            if target.resolve() == source.resolve() or (target.exists() and source.exists() and target.samefile(source)):
                raise ValueError("output must not alias an input file")
    try:
        graph = parse_graph(_read(args.graph))
    except UnicodeDecodeError as error:
        raise GraphFormatError("graph must contain ASCII text") from error
    ref = Reference(graph, args.h, max_vertices=args.max_vertices)
    record = {"schema_version": 1, "kind": "reference_" + args.command,
              "graph_sha256": graph_sha256(graph), "h": ref.h, "seed": args.seed,
              "vertices": list(graph.vertices), "edges": [list(edge) for edge in graph.edges]}
    if args.command == "truth":
        ranked = direct_lhcds(ref, k=args.k)
        record.update(selection={"mode": "all" if args.all else "fixed_k", "k": args.k},
                      results=solution_records(ref, ranked))
    elif args.command == "oracle":
        if args.x is None:
            result = exhaustive_F(ref, args.parameter)
        else:
            x, y = parse_set(_read(args.x), graph), parse_set(_read(args.y), graph)
            result = exhaustive_restricted(ref, args.parameter, x, y)
        record.update(bounds={"x": list(graph.ids(result.x)), "y": list(graph.ids(result.y))},
                      result=oracle_record(ref, result), objective_scaled=decimal_text(result.objective_scaled),
                      maximizers=[list(graph.ids(s)) for s in result.maximizers])
    else:
        chain = cardinality_line_chain(ref)
        record.update(chain=[list(graph.ids(s)) for s in chain.sets],
                      breakpoints=[fraction_record(b) for b in chain.breakpoints],
                      cardinality_maxima=[decimal_text(count) for count in chain.cardinality_maxima],
                      intersections=[fraction_record(b) for b in chain.intersections],
                      sentinel=fraction_record(chain.sentinel),
                      samples=[oracle_record(ref, sample) for sample in chain.samples])
    _write_output(args.output, json_line(record))


def main(argv=None) -> int:
    status, code, message = "completed", 0, None
    try:
        arguments = sys.argv[1:] if argv is None else list(argv)
        # argparse normally accepts duplicate options; the frozen domain rejects them.
        options = [arg.split("=", 1)[0] for arg in arguments if arg.startswith("--")]
        if len(options) != len(set(options)):
            raise ValueError("duplicate option")
        _execute(_parser().parse_args(arguments))
    except SizeLimitError as error:
        status, code, message = "resource_limit", 5, str(error)
    except GraphFormatError as error:
        status, code, message = "invalid_graph", 3, str(error)
    except ValueError as error:
        status, code, message = "invalid_argument", 2, str(error)
    except OSError as error:
        status, code, message = "io_error", 4, str(error)
    except MemoryError:
        status, code, message = "oom", 6, "allocation failed"
    except KeyboardInterrupt:
        status, code, message = "incomplete", 7, "interrupted"
    except Exception as error:
        status, code, message = "internal_error", 9, str(error)
    report = {"schema_version": 1, "status": status, "complete": code == 0,
              "output_count": 1 if code == 0 else 0, "semantic_sha256": None}
    if message is not None:
        report["message"] = message
    try:
        sys.stderr.write(json_line(report))
        sys.stderr.flush()
    except OSError:
        return 4
    return code

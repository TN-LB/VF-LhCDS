"""Tiny simple graphs with explicit original IDs and ordinary connectivity (T01)."""

from dataclasses import dataclass, field
from typing import Iterable


def require_integer(value: int, name: str, minimum: int | None = None) -> int:
    if type(value) is not int or (minimum is not None and value < minimum):
        raise ValueError(f"{name} must be an integer" + (f" >= {minimum}" if minimum is not None else ""))
    return value


@dataclass(frozen=True)
class Graph:
    """Canonical numeric IDs; bit i always refers to vertices[i]. No implied vertices."""

    vertices: tuple[int, ...]
    edges: tuple[tuple[int, int], ...]
    adjacency: tuple[int, ...] = field(init=False, repr=False)

    def __post_init__(self):
        vertices = tuple(self.vertices)
        edges = tuple(tuple(edge) for edge in self.edges)
        for vertex in vertices:
            require_integer(vertex, "vertex ID")
        if not vertices or vertices != tuple(sorted(set(vertices))):
            raise ValueError("Graph requires nonempty, sorted, distinct original IDs")
        index = {vertex: i for i, vertex in enumerate(vertices)}
        adjacency = [0] * len(vertices)
        for edge in edges:
            if len(edge) != 2:
                raise ValueError("edge must have two endpoints")
            u, v = edge
            require_integer(u, "edge endpoint")
            require_integer(v, "edge endpoint")
            if u not in index or v not in index or u >= v:
                raise ValueError("edges require declared endpoints with u < v")
            adjacency[index[u]] |= 1 << index[v]
            adjacency[index[v]] |= 1 << index[u]
        if edges != tuple(sorted(set(edges))):
            raise ValueError("Graph requires sorted, distinct edges")
        object.__setattr__(self, "vertices", vertices)
        object.__setattr__(self, "edges", edges)
        object.__setattr__(self, "adjacency", tuple(adjacency))

    @property
    def n(self) -> int:
        return len(self.vertices)

    @property
    def full_mask(self) -> int:
        return (1 << self.n) - 1

    def check_mask(self, mask: int) -> int:
        require_integer(mask, "vertex mask", 0)
        if mask > self.full_mask:
            raise ValueError("vertex mask contains undeclared vertices")
        return mask

    def mask(self, vertices: Iterable[int]) -> int:
        index = {vertex: i for i, vertex in enumerate(self.vertices)}
        result = 0
        for vertex in vertices:
            require_integer(vertex, "vertex ID")
            if vertex not in index:
                raise ValueError("set contains an undeclared vertex")
            bit = 1 << index[vertex]
            if result & bit:
                raise ValueError("set contains a duplicate vertex")
            result |= bit
        return result

    def ids(self, mask: int) -> tuple[int, ...]:
        self.check_mask(mask)
        return tuple(v for i, v in enumerate(self.vertices) if mask & (1 << i))

    def components(self, mask: int) -> tuple[int, ...]:
        self.check_mask(mask)
        remaining, components = mask, []
        while remaining:
            todo = remaining & -remaining
            component = 0
            while todo:
                bit = todo & -todo
                todo ^= bit
                component |= bit
                todo |= self.adjacency[bit.bit_length() - 1] & mask & ~component
            components.append(component)
            remaining &= ~component
        return tuple(components)

    def connected(self, mask: int) -> bool:
        return len(self.components(mask)) == 1


@dataclass(frozen=True)
class Normalization:
    graph: Graph
    removed_self_loops: int
    removed_duplicate_edges: int


def normalize_graph(vertices: Iterable[int], edges: Iterable[tuple[int, int]]) -> Normalization:
    """Raw normalization only: capture V first, then remove loops/duplicate edges.

    The canonical file reader separately rejects loops and duplicates.
    """
    declared = tuple(vertices)
    for vertex in declared:
        require_integer(vertex, "vertex ID")
    if not declared or len(set(declared)) != len(declared):
        raise ValueError("declare a nonempty universe with distinct vertex IDs")
    universe = set(declared)
    kept = set()
    loops = duplicates = 0
    for edge in edges:
        edge = tuple(edge)
        if len(edge) != 2:
            raise ValueError("edge must have two endpoints")
        u, v = edge
        require_integer(u, "edge endpoint")
        require_integer(v, "edge endpoint")
        if u not in universe or v not in universe:
            raise ValueError("edge endpoint was not declared")
        if u == v:
            loops += 1
        else:
            pair = (min(u, v), max(u, v))
            if pair in kept:
                duplicates += 1
            kept.add(pair)
    return Normalization(Graph(tuple(sorted(declared)), tuple(sorted(kept))), loops, duplicates)

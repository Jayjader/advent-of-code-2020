from __future__ import annotations

from dataclasses import dataclass
from itertools import groupby, chain
from typing import TypeAlias

Vertex: TypeAlias = int
Start: TypeAlias = Vertex
End: TypeAlias = Vertex
Edge: TypeAlias = tuple[Start, End]


@dataclass
class Graph:
    vertexes: set[Vertex]
    edges: dict[Start, set[End]]


def make_graph(input_edges: list[Edge]) -> Graph:
    return Graph(
        vertexes=set(chain.from_iterable(input_edges)),
        edges={
            v_start: {edge[1] for edge in edges}
            for v_start, edges in groupby(input_edges, lambda edge: edge[0])
        },
    )


def paths_to_end(graph: Graph) -> int:
    """
    paths_to_end_from(node) = sum(paths_to_end_from(start) for start in leads_to(node))
    """

    paths = {max(graph.vertexes): 1}
    for vert in sorted(graph.vertexes, reverse=True):
        paths_for_vert = (
            1
            if (successors := graph.edges.get(vert)) is None
            else sum(paths[successor] for successor in successors)
        )
        paths[vert] = paths_for_vert
    return paths[min(graph.vertexes)]

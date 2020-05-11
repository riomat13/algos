#!/usr/bin/env python3

import collections
from typing import List

from graph.base import Graph


def kahn_sort(G: Graph) -> List[int]:
    """Topological sort by Kahn's Algorithm."""
    in_degree = [0] * G.V

    for u in range(G.V):
        for edge in G.g(u):
            in_degree[edge.v] += 1

    vertices = collections.deque()
    order = []

    for u in range(G.V):
        if in_degree[u] == 0:
            vertices.append(u)

    while vertices:
        u = vertices.popleft()
        order.append(u)

        for edge in G.g(u):
            in_degree[edge.v] -= 1
            if in_degree[edge.v] == 0:
                vertices.append(edge.v)

    # return empty if not DAG
    return order if len(order) == G.V else []

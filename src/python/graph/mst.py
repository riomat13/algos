#!/usr/bin/env python3

import heapq


def prims(s: int, G: 'UDGraph') -> list:
    """Minimum spanning tree by Prim's Algorithm.

    Args:
        s: int
            source node for Prim's Algorithm
        G: UDGraph
            undirected graph object
    Returns:
        edges: list(UDEdge)
           list of edge object for connection
           if source, set as None
    """
    edges = [None] * G.V
    visited = {s}

    hq = []

    for e in G.g(s):
        heapq.heappush(hq, (e, s))

    while hq:
        edge, s = heapq.heappop(hq)
        v = edge.oppose(s)
        if v in visited:
            continue

        edges[v] = edge
        visited.add(v)

        for e in G.g(v):
            if e.oppose(v) not in visited:
                heapq.heappush(hq, (e, v))

    return edges

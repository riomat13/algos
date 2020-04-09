#!/usr/bin/env python3

import heapq


def dijkastra(s: int, G: 'UDGraph') -> list:
    """Shortest path from source to all vertices.

    Args:
        s: int
            source node
        G: UDGraph
            undirected graph object which represents
            the edges by UDEdge object
    Returns:
        path: list
            list of parent node, -1 if root
        dist: list
            list of cost to each node from source
    """
    dist = [float('inf')] * G.V
    path = [-1] * G.V

    # set 0 at source node
    dist[s] = 0

    visited = {s}

    hq = []

    for e in G.g(s):
        heapq.heappush(hq, (e.w, s, e.oppose(s)))

    while hq:
        w, s, v = heapq.heappop(hq)

        if v in visited:
            continue

        if w < dist[v]:
            dist[v] = w
            path[v] = s

        visited.add(s)

        for e in G.g(v):
            heapq.heappush(hq, (e.w + dist[v], v, e.oppose(v)))

    return path, dist


class FloydWarshall(object):
    """Floyd Warshall to find shortest path.

    Detail:
    https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm
    """
    def __init__(self, G: 'Graph'):
        dist = [[float('inf')] * G.V for _ in range(G.V)]
        path = [[-1] * G.V for _ in range(G.V)]

        # set weights on all edges to dist matrix
        for u in range(G.V):
            for e in G.g(u):
                dist[e.u][e.v] = e.w
                path[e.u][e.v] = e.v

        for v in range(G.V):
            dist[v][v] = 0
            path[v][v] = v

        for k in range(G.V):
            for i in range(G.V):
                for j in range(G.V):
                    if i != j and dist[i][j] > dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        path[i][j] = path[i][k]

        self._dist = dist
        self._path = path

    def get_path(self, s, v) -> (list, list):
        """Return shortest path from source to destination.

        Args:
            s: int
                source vertex
            v: int
                target vertex
        Returns:
            path: list of int
                path to target
            cost: list of int, float
                list of costs for each step
        """
        path = [s]
        cost = [0]

        while s != v:
            if s == -1:
                return [], []

            cost.append(self._dist[s][self._path[s][v]])
            s = self._path[s][v]
            path.append(s)

        return path, cost

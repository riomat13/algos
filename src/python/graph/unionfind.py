#!/usr/bin/env python3


class UF(object):
    def __init__(self, n: int):
        self._n = n
        self.parent = list(range(n+1))
        self._count = n
        self.rank = [1] * (n + 1)

    @property
    def count(self):
        return self._count

    def _validate(self, v):
        if v < 0 or v > self._n:
            raise ValueError('Given vertex is out of range')

    def find(self, v: int) -> int:
        self._validate(v)

        while (self.parent[v] != v):
            self.parent[v] = self.parent[self.parent[v]]
            v = self.parent[v]
        return v

    def union(self, u: int, v: int) -> None:
        root_u = self.find(u)
        root_v = self.find(v)

        if root_u == root_v:
            return

        if self.rank[root_u] > self.rank[root_v]:
            self.parent[v] = root_u
        elif self.rank[root_v] > self.rank[root_u]:
            self.parent[u] = root_v
        else:
            self.parent[v] = root_u
            self.rank[root_u] += 1
        self._count -= 1

    def connected(self, u: int, v: int) -> bool:
        return self.find(u) == self.find(v)

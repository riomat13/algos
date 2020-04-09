#!/usr/bin/env python3

import random


class UnorderedList(list):
    """List with a feature to get k-th smallest value.
    If send query to get k-th smallest value multiple times,
    this will be no longer efficient.

    While processing to get k-th smallest value,
    list values are swapped in-place,
    hence, there is no consistency in index.

    Usage:
        >>> l = UnorderedList([1, 5, 4, 2, 7, 3, 6])
        >>> l.kth_smallest(4)
        4
        >>> l.kth_smallest(6)
        6
        >>> random.shuffle(l)
        >>> l.kth_smallest(5)
        5
    """
    def _partition(self, l, r):
        idx = random.randint(l, r)
        pivot = self[idx]
        self[idx], self[r] = self[r], self[idx]
        idx = r
        r -= 1
        i = l

        while i <= r:
            if self[i] > pivot:
                self[i], self[r] = self[r], self[i]
                r -= 1
            elif self[i] < pivot:
                self[i], self[l] = self[l], self[i]
                l += 1
                i += 1
            else:
                i += 1
        self[idx], self[l] = self[l], self[idx]
        return l

    def _select(self, k):
        l, r = 0, self.__len__() - 1
        idx = 0
        while True:
            idx = self._partition(l, r)

            if idx == k - 1:
                return self[k-1]
            elif idx < k - 1:
                l = idx + 1
            else:
                r = idx - 1

    def kth_smallest(self, k):
        return self._select(k)

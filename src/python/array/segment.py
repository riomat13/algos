#!/usr/bin/env python3

import math


class SegmentTree(object):
    def __init__(self, arr):
        self._size = len(arr)
        node_size = 2 * (1 << math.ceil(math.log2(self._size))) + 1
        self.tree = [0] * node_size
        self._construct_tree(0, 0, self._size-1, arr)

    def _construct_tree(self, node, l, r, arr):
        if l == r:
            self.tree[node] = arr[l]
        else:
            mid = (l + r) // 2
            self._construct_tree(node*2+1, l, mid, arr)
            self._construct_tree(node*2+2, mid+1, r, arr)

            self.tree[node] = self.tree[node*2+1] + self.tree[node*2+2]

    def update(self, index, val):
        """Update value in array.

        Args:
            index: int
                target index in array to update
            val: int
                value to be updated

        Returns:
            None
        """
        pass
    
    def _get_sum(self, node, l, r, st, end):
        if r < st or end < l:
            return 0
        if l <= st and end <= r:
            return self.tree[node]

        mid = (st + end) // 2

        return self._get_sum(2*node, l, mid, st, end) + \
                self._get_sum(2*node+1, mid+1, r, st, end)

    def get_sum(self, st, end):
        """Get sum in the range of [st, end] in array.

        Args:
            st: int
                index of starting point
            end: int
                index of end point inclusive

        Returns:
            total: int
                partial sum of the array in given range

        Exceptions:
            ValueError: if st > end
            IndexError: if out of range
        """
        if st > end:
            raise ValueError('Starting point must be smaller or equal to the end point')
        if st < 0 or end >= self._size:
            raise IndexError(f'Index out of range. The range is [0, {self._size})')

        return self._get_sum(0, 0, self._size-1, st, end)

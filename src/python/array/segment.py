#!/usr/bin/env python3

import math as _math


class SegmentTree(object):
    def __init__(self, size):
        self._size = size
        node_size = 2 * (1 << _math.ceil(_math.log2(self._size))) + 1
        self._tree = [0] * node_size

    def get_list(self):
        """Return original array."""
        return self._arr[:]

    def _construct_tree(self, node, l, r, arr):
        if l == r:
            self._tree[node] = arr[l]
        else:
            mid = (l + r) // 2
            self._construct_tree(node*2+1, l, mid, arr)
            self._construct_tree(node*2+2, mid+1, r, arr)

            self._tree[node] = self._tree[node*2+1] + self._tree[node*2+2]

    def _update(self, node, l, r, index, diff):
        if index < l or r < index:
            return

        self._tree[node] -= diff

        if l == r:
            return

        mid = (l + r) // 2
        self._update(node*2+1, l, mid, index, diff)
        self._update(node*2+2, mid+1, r, index, diff)

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
        diff = self._arr[index] - val
        self._arr[index] = val
        self._update(0, 0, self._size - 1, index, diff)


    def _get_sum(self, node, l, r, st, end):
        if r < st or end < l:
            return 0
        if st <= l and r <= end:
            return self._tree[node]

        mid = (l + r) // 2

        return self._get_sum(2*node+1, l, mid, st, end) + \
                self._get_sum(2*node+2, mid+1, r, st, end)

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

    @classmethod
    def from_array(cls, array):
        cls = cls(len(array))
        cls._arr = array
        cls._construct_tree(0, 0, cls._size-1, array)
        return cls

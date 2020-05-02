#!/usr/bin/env python3

import random
from typing import List


def _qsort(st, end, arr):
    if st >= end:
        return
    if end - st == 1:
        if arr[st] > arr[end]:
            arr[st], arr[end] = arr[end], arr[st]

        return

    pivot = random.randint(st, end)
    arr[pivot], arr[end] = arr[end], arr[pivot]

    target = arr[end]
    left = st

    for i in range(st, end):
        if arr[i] < target:
            arr[i], arr[left] = arr[left], arr[i]
            left += 1
    arr[left], arr[end] = arr[end], arr[left]

    _qsort(st, left-1, arr)
    _qsort(left+1, end, arr)


def quick_sort(arr: List[int]) -> None:
    """In-place quick sort."""
    _qsort(0, len(arr)-1, arr)

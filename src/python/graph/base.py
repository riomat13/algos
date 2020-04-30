#!/usr/bin/env python3

import random
import collections
import functools
from typing import List


class Node(object):
    def __init__(self, val, order='in'):
        self._left = None
        self._right = None
        self._val = val
        self.set_order_type(order)

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    @property
    def val(self):
        return self._val

    def set_order_type(self, order='in') -> None:
        if order not in ('in', 'pre'):
            raise ValueError('Order type must be chosen from (`in`, `pre`)')

        self._order_type = order

    def __iter__(self):
        if self._order_type == 'in':
            yield from self._inorder(self)
        elif self._order_type == 'pre':
            yield from self._preorder(self)

    def _inorder(self, node):
        if node.left is not None:
            yield from self._inorder(node.left)

        yield node.val

        if node.right is not None:
            yield from self._inorder(node.right)

    def _preorder(self, node):
        yield node.val

        if node.left is not None:
            yield from self._preorder(node.left)

        if node.right is not None:
            yield from self._preorder(node.right)

    def print_inorder(self) -> None:
        """Print out all nodes inorder."""
        print(*self._inorder(self))

    def print_preorder(self) -> None:
        """Print out all nodes preorder."""
        print(*self._preorder(self))


class LinkedList(object):

    def __init__(self, root=None):
        self.root = root
        self.tail = root
        self._size = int(root is not None)

    @property
    def size(self):
        return self._size

    def add_node(self, val: int) -> None:
        if self.root is None:
            self.root = LinkNode(val)
            self.tail = self.root
        else:
            self.tail.next = LinkNode(val)
            self.tail = self.tail.next
        self._size += 1

    def find(self, val: int) -> bool:
        """Find if target value is in linked list by linear search."""
        if self.root is None:
            return False

        node = self.root
        while node:
            if node.val == val:
                return True
            node = node.next
        return False

    def delete(self, val: int) -> bool:
        """Delete the target value.
        Return True if successed, other wise False.
        """
        if self.root.val == val:
            self.root = self.root.next
            self._size -= 1
            return True

        node = self.root
        while node.next:
            if val == node.next.val:
                node.next = node.next.next
                self._size -= 1
                return True
            node = node.next
        return False


    def parse_vals(self) -> List[int]:
        """Return all values stored in linked list."""
        if self.root is None:
            return []

        node = self.root
        vals = [0] * self.size

        for i in range(self._size):
            vals[i] = node.val
            node = node.next

        return vals


class LinkNode(object):
    """Linked List node."""
    def __init__(self, val, next=None):
        self.next = next
        self.val = val


class ExtLinkNode(object):
    """Doubly Linked List node."""
    def __init__(self, val, next=None, prev=None):
        self.next = next
        self.prev = prev
        self.val = val


@functools.total_ordering
class Edge(object):
    """Directed edge which is comparable by the weights."""
    def __init__(self, u: int, v: int, w: float):
        self._u = u
        self._v = v
        self.w = w

    @property
    def u(self):
        return self._u

    @property
    def v(self):
        return self._v

    def __str__(self):
        return f'Edge: {self._u} -> {self._v}: {self.w}'

    def __eq__(self, other):
        return self.w == other.w

    def __lt__(self, other):
        return self.w < other.w


class UDEdge(Edge):
    """Undirected Edge object."""
    def __init__(self, u: int, v: int, w: (int,float)):
        """Undirected edge.

        Args:
            u: int
                vertex from one side
            v: int
                vertex from another side
            w: int or floar
                edge weight
        """
        if u > v:
            u, v = v, u
        super(UDEdge, self).__init__(u, v, w)

    def oppose(self, u):
        if u != self.u and u != self.v:
            raise ValueError(f'edge does not have node: {u}')
        return self.v if u == self.u else self.u

    def __str__(self):
        return f'Edge: {self.u:2d} <-> {self.v:2d}: {self.w:5.2f}'

    def __repr__(self):
        return f'UDEdge({self.u},{self.v},{self.w})'


class Graph(object):
    """Directed Graph."""
    def __init__(self, n):
        self._vertices = n
        self._g = collections.defaultdict(list)

    @property
    def V(self):
        return self._vertices

    def _validate(self, n):
        if n < 0 or n > self._vertices:
            raise ValueError(f'Invalid vertex: {n}')

    def add_edge(self, u, v, w=0):
        self._validate(u)
        self._validate(v)
        e = Edge(u, v, w)
        self._g[u].append(e)

    def g(self, u):
        return self._g[u][:]

    def print_edges(self):
        for s, vertices in self._g.items():
            for v in vertices:
                print(v)


class UDGraph(Graph):
    """Undirected Graph."""
    def __init__(self, n):
        self._vertices = n
        self._g = collections.defaultdict(list)

    def add_edge(self, u, v, w=0):
        self._validate(u)
        self._validate(v)
        e = UDEdge(u, v, w)
        self._g[e.u].append(e)
        self._g[e.v].append(e)

    def print_edges(self):
        for u in range(self._vertices):
            for e in self._g[u]:
                if e.u == u:
                    print(e)


def generate_random_nodes(n=10, shuffle=False, random_split=False):
    vertices = list(range(1, n+1))

    if shuffle:
        random.shuffle(vertices)

    root = Node(vertices.pop())

    def _gen(node, n_items, random_split):
        if n_items == 0:
            return

        if random_split:
            left = random.randint(1, n_items)
        else:
            left = n_items // 2
        right = n_items - left

        if left > 0:
            node.left = Node(vertices.pop())
            _gen(node.left, left-1, random_split)
        if right > 0:
            node.right = Node(vertices.pop())
            _gen(node.right, right-1, random_split)

    _gen(root, n-1, random_split)

    return root


def generate_balanced_binary_tree(n=7):
    arr = list(range(n+1))

    def recur(l, r):
        if l > r:
            return None
        if l == r:
            return Node(arr[l])

        mid = (l + r) // 2
        node = Node(arr[mid])
        node._left = recur(l, mid-1)
        node._right = recur(mid+1, r)
        return node

    return recur(1, n)

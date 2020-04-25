#!/usr/bin/env python3

from graph.base import Node


RED = True


class RBNode(Node):
    def __init__(self, val, order='in'):
        super(RBNode, self).__init__(val, order)
        self.color = RED
        self._size = 1

    @property
    def size(self):
        return self._size

    def set_left(self, node: 'RBNode') -> None:
        if node is not None:
            self._left = node
            self._size = node.size + self._get_size(node.right) + 1

    def set_right(self, node: 'RBNode') -> None:
        if node is not None:
            self._right = node
            self._size = node.size + self._get_size(node.left) + 1

    @staticmethod
    def _get_size(node):
        if node is None:
            return 0
        return node.size


class RBTree(object):
    """Red-Black Tree."""
    def __init__(self):
        self.root = None

    @property
    def size(self):
        return self.root.size

    def rotate_left(self, node: RBNode) -> RBNode:
        head = node.right
        node._right = head.left
        head._left = node
        head.color = head.left.color
        head._left.color = RED
        head._size = node._size
        node._size = node._get_size(node.left) + node._get_size(node.right) + 1
        return head

    def rotate_right(self, node: RBNode) -> RBNode:
        head = node.left
        node._left = head.right
        head._right = node
        head.color = head.right.color
        head._right.color = RED
        head._size = node._size
        node._size = node._get_size(node.left) + node._get_size(node.right) + 1
        return head

    def flip(self, node: RBNode) -> RBNode:
        node.color ^= node.color
        node.left.color ^= node.left.color
        node.right.color ^= node.right.color
        return node

    def __iter__(self):
        yield from self.root._inorder(self.root)

    def _add_node(self, node, val):
        if node is None:
            return RBNode(val)

        # skip if already the node exists
        if node.val == val:
            return node

        if node.val < val:
            node._right = self._add_node(node.right, val)
        elif node.val > val:
            node._left = self._add_node(node.left, val)

        if self._is_red(node.right) and not self._is_red(node.left):
            node = self.rotate_left(node)
        if self._is_red(node.left) and self._is_red(node.left.left):
            node = self.rotate_right(node)
        if self._is_red(node.left) and self._is_red(node.right):
            node = self.flip(node)

        node._size = RBNode._get_size(node.left) + RBNode._get_size(node.right) + 1

        return node

    def add_node(self, val: int) -> None:
        """Add node with given value.

        If the node already exists, skip the operation.

        Args:
            val: int
                value of new node

        Returns:
            None
        """
        self.root = self._add_node(self.root, val)
        self.root.color = not RED

    def _is_red(self, node):
        if node is None:
            return False
        return node.color

    def _find(self, node, val):
        if node is None:
            return False
        if node.val == val:
            return True
        if node.val > val:
            return self._find(node.left, val)
        else:
            return self._find(node.right, val)

    def find(self, val: int) -> bool:
        """Find value in Red-black tree.

        Args:
            val: int
                target value

        Returns:
            bool: True if exists, False otherwise.
        """
        return self._find(self.root, val)

    @classmethod
    def from_array(cls, arr: list) -> 'RBTree':
        """Build tree from array."""
        cls = cls()
        cls.root = RBNode(arr[0])
        for val in arr[1:]:
            cls.add_node(val)

        return cls

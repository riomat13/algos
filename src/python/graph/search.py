#!/usr/bin/env python3

from graph.base import Node


def morris_inorder(node):
    while node is not None:
        if node.left is None:
            yield node.val
            node = node.right
        else:
            tmp = node.left
            while tmp.right is not None and \
                    tmp.right is not node:
                tmp = tmp.right

            if tmp.right is None:
                tmp.right = node
                node = node.left
                continue

            tmp.right = None
            yield node.val
            node = node.right


def morris_preorder(node):
    while node is not None:
        if node.left is None:
            yield node.val
            node = node.right
        else:
            tmp = node.left
            while tmp.right is not None and tmp.right is not node:
                tmp = tmp.right

            if tmp.right is None:
                tmp.right = node
                yield node.val
                node = node.left
                continue

            tmp.right = None
            node = node.right

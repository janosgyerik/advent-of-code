#!/usr/bin/env python3

import sys
from collections import defaultdict


class TreeNode:
    def __init__(self):
        self.parent = None
        self.children = []


def ancestors(node):
    if node is None:
        return

    yield from ancestors(node.parent)

    yield node


def main():
    nodes = defaultdict(lambda: TreeNode())
    for line in sys.stdin.readlines():
        parent, child = line.rstrip().split(')')
        nodes[parent].children.append(nodes[child])
        nodes[child].parent = nodes[parent]

    ancestors_of_you = ancestors(nodes['YOU'])
    ancestors_of_san = ancestors(nodes['SAN'])

    while True:
        if next(ancestors_of_you) != next(ancestors_of_san):
            break

    print(sum(1 for _ in ancestors_of_you) + sum(1 for _ in ancestors_of_san))


if __name__ == '__main__':
    main()

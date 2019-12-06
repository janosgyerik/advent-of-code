#!/usr/bin/env python3

import sys
from collections import defaultdict


class TreeNode:
    def __init__(self):
        self.children = []


def heights(node, height):
    yield height - 1
    for child in node.children:
        yield from heights(child, height + 1)


def main():
    nodes = defaultdict(lambda: TreeNode())
    for line in sys.stdin.readlines():
        parent, child = line.rstrip().split(')')
        nodes[parent].children.append(nodes[child])

    print(sum(heights(nodes['COM'], 1)))


if __name__ == '__main__':
    main()

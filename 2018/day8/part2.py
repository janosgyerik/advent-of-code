#!/usr/bin/env python

import sys


class Node:
    def __init__(self):
        self.children = []
        self.meta = []

    def value(self, n=0):
        if n:
            if n <= len(self.children):
                return self.children[n-1].value()
            return 0

        if not self.children:
            return sum(self.meta)

        return sum(self.value(m) for m in self.meta)

stack = []
numbers = (int(v) for v in sys.stdin.readline().split())
root = Node()
stack.append((root, next(numbers), next(numbers), 0))
while stack:
    parent, children, meta, i = stack.pop()
    if children == i:
        parent.meta = [next(numbers) for _ in range(meta)]
        continue

    stack.append((parent, children, meta, i + 1))

    child = Node()
    parent.children.append(child)

    stack.append((child, next(numbers), next(numbers), 0))

print(root.value())

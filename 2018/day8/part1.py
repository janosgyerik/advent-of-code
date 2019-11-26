#!/usr/bin/env python

import sys

stack = []
total = 0
numbers = (int(v) for v in sys.stdin.readline().split())
stack.append((next(numbers), next(numbers), 0))
while stack:
    children, meta, i = stack.pop()
    if children == i:
        for _ in range(meta):
            total += next(numbers)
        continue

    stack.append((children, meta, i + 1))
    stack.append((next(numbers), next(numbers), 0))

print(total)

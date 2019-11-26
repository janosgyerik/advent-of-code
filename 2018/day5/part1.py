#!/usr/bin/env python

import sys


def react(a, b):
    return a != b and (a.lower() == b or a.upper() == b)

s = sys.stdin.readlines()[0].rstrip()
stack = list()
for c in s:
    if not stack:
        stack.append(c)
        continue

    if react(stack[-1], c):
        stack.pop()
        continue

    stack.append(c)

print(len(stack))

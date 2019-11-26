#!/usr/bin/env python

import sys, re, string


def react(a, b):
    return a != b and (a.lower() == b or a.upper() == b)


def reduced_length(s):
    stack = list()
    for c in s:
        if not stack:
            stack.append(c)
            continue

        if react(stack[-1], c):
            stack.pop()
            continue

        stack.append(c)

    return len(stack)


def min_reduced_length(s):
    return min(reduced_length(re.sub(t, '', s, flags=re.IGNORECASE)) for t in string.lowercase)


line = sys.stdin.readlines()[0].rstrip()
print(min_reduced_length(line))

#!/usr/bin/env python
import re
import sys
from collections import namedtuple, Counter, deque, defaultdict
from itertools import product
from heapq import heappush, heappop, heapify
from functools import lru_cache


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


scoremap = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}


parens = {
    '(': ')',
    '<': '>',
    '[': ']',
    '{': '}',
}


openers = parens.keys()


def find_illegal(s):
    stack = []
    for c in s:
        if c in openers:
            stack.append(c)
        else:
            if not stack:
                return c
            if c != parens[stack[-1]]:
                return c

            stack.pop()


def solve(lines):
    total = 0
    for line in lines:
        illegal = find_illegal(line)
        if illegal:
            total += scoremap[illegal]

    return total


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines))


if __name__ == '__main__':
    main()

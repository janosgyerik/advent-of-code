#!/usr/bin/env python

import sys
from collections import namedtuple, Counter, deque, defaultdict
from itertools import product
from heapq import heappush, heappop, heapify
from functools import lru_cache


def ints(line):
    return [int(x) for x in line.split(' ')]


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


def priority(x):
    if x.isupper():
        return ord(x) - ord('A') + 27

    return ord(x) - ord('a') + 1


def solve(lines):
    total = 0
    for i in range(0, len(lines), 3):
        a, b, c = lines[i], lines[i + 1], lines[i + 2]
        common = set(a).intersection(set(b)).intersection(set(c))
        assert len(common) == 1

        (common,) = common
        total += priority(common)

    return total


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines))


if __name__ == '__main__':
    main()

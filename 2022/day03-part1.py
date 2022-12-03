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


def find_common(left, right):
    x = set(left).intersection(set(right))
    assert len(x) == 1
    (x,) = x
    return x


def priority(x):
    if x.isupper():
        return ord(x) - ord('A') + 27

    return ord(x) - ord('a') + 1


def solve(lines):
    total = 0
    for line in lines:
        half = len(line) // 2
        left = line[:half]
        right = line[half:]
        assert len(left) == len(right)
        assert len(left) + len(right) == len(line)

        common = find_common(left, right)
        total += priority(common)

    return total


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines))


if __name__ == '__main__':
    main()

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


def solve(lines):
    count = 0
    for line in lines:
        left, right = line.split(',')
        s1, e1 = left.split('-')
        s2, e2 = right.split('-')
        s1, e1, s2, e2 = [int(x) for x in [s1, e1, s2, e2]]
        if (
                False
                or s1 <= s2 <= e1
                or s1 <= e2 <= e1
                or s2 <= s1 <= e2
                or s2 <= e1 <= e2
        ):
            count += 1

    return count


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines))


if __name__ == '__main__':
    main()

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


def parse_input(lines):
    return [int(x) for x in lines[0].split(',')]


def nsum(n):
    return n * (n + 1) // 2


def compute_cost(crabs, pos):
    return sum(nsum(abs(x - pos)) for x in crabs)


def min_fuel(crabs):
    def derivative(p):
        return compute_cost(crabs, p) - compute_cost(crabs, p - 1)

    left = min(crabs)
    right = max(crabs)
    while left < right:
        mid = left + (right - left) // 2
        if derivative(left) * derivative(mid) < 0:
            right = mid
        else:
            left = mid + 1

    return compute_cost(crabs, left - 1)


def solve(lines):
    crabs = parse_input(lines)
    return min_fuel(crabs)


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines))


if __name__ == '__main__':
    main()

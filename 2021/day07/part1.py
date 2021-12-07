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


def compute_cost(crabs, pos):
    return sum(abs(x - pos) for x in crabs)


def min_fuel(crabs):
    unique_crabs = sorted(set(crabs))
    min_cost = compute_cost(crabs, unique_crabs[0])
    for index in range(1, len(unique_crabs)):
        cost = compute_cost(crabs, unique_crabs[index])
        if min_cost < cost:
            return min_cost

        min_cost = cost


def solve(lines):
    crabs = parse_input(lines)
    return min_fuel(crabs)


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines))


if __name__ == '__main__':
    main()

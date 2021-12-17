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


def simulate(counts):
    new_counts = defaultdict(int)
    for k, v in counts.items():
        if k == 0:
            new_counts[8] = v
            new_counts[6] += v
        else:
            new_counts[k-1] += v

    return new_counts


def solve(lines):
    fishes = parse_input(lines)
    counts = Counter(fishes)
    for _ in range(80):
        counts = simulate(counts)
    return sum(counts.values())


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines))


if __name__ == '__main__':
    main()

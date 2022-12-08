#!/usr/bin/env python
import functools
import sys
from collections import namedtuple, Counter, deque, defaultdict
from dataclasses import dataclass
from functools import lru_cache
from heapq import heappush, heappop, heapify
from itertools import product


def ints(line):
    return [int(x) for x in line.split(' ')]


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


def score(grid, r, c):
    dim = len(grid)
    start = grid[r][c]
    scores = []

    # up, left, down, right
    for dr, dc in ((-1, 0), (0, -1), (1, 0), (0, 1)):
        r2, c2 = r, c
        dist = 0
        while True:
            r2 += dr
            c2 += dc
            if not (0 <= r2 < dim and 0 <= c2 < dim):
                break

            dist += 1

            current = grid[r2][c2]
            if current >= start:
                break

        scores.append(dist)

    return functools.reduce(lambda a, b: a * b, scores)


def solve(lines):
    dim = len(lines)
    grid = [[int(x) for x in line] for line in lines]

    best = 0
    for r in range(dim):
        for c in range(dim):
            best = max(best, score(grid, r, c))

    return best


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines))


if __name__ == '__main__':
    main()

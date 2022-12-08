#!/usr/bin/env python

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


def count_in_direction(grid, r, c, dr, dc, counted):
    dim = len(grid)

    r2, c2 = r, c
    count = 0
    highest = -1
    while True:
        current = grid[r2][c2]
        if current > highest:
            if (r2, c2) not in counted:
                count += 1
                counted.add((r2, c2))
            highest = current

        r2 += dr
        c2 += dc
        if not (0 <= r2 < dim and 0 <= c2 < dim):
            break

    return count


def solve(lines):
    dim = len(lines)
    grid = [[int(x) for x in line] for line in lines]

    counted = set()
    count = 0
    for r in range(dim):
        count += count_in_direction(grid, r, 0, 0, 1, counted)
        count += count_in_direction(grid, r, dim - 1, 0, -1, counted)
    for c in range(dim):
        count += count_in_direction(grid, 0, c, 1, 0, counted)
        count += count_in_direction(grid, dim - 1, c, -1, 0, counted)

    return count


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines))


if __name__ == '__main__':
    main()

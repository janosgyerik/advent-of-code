#!/usr/bin/env python
import functools
import sys
from collections import namedtuple, Counter, deque, defaultdict
from dataclasses import dataclass
from functools import lru_cache
from heapq import heappush, heappop, heapify
from itertools import product
from typing import Callable, List

from utils.binary_search import binary_search


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


def parse_paths(lines):
    paths = []
    for line in lines:
        path = []
        paths.append(path)
        for point in line.split(' -> '):
            r, c = [int(x) for x in point.split(',')]
            path.append((r, c))

    return paths


class Grid:
    def __init__(self, paths):
        min_c = min(min(segment[0] for segment in path) for path in paths)
        min_r = min(min(segment[1] for segment in path) for path in paths)
        max_c = max(max(segment[0] for segment in path) for path in paths)
        max_r = max(max(segment[1] for segment in path) for path in paths)
        max_r += 2
        max_c += max_r

        self.grid = [['.'] * (max_c + 1) for _ in range(max_r + 1)]
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])

        paths.append([(0, max_r), (max_c, max_r)])

        self._mark_rocks(paths)

    def _mark_rocks(self, paths):
        for path in paths:
            for p0, p1 in zip(path[:-1], path[1:]):
                c0, r0 = p0
                c1, r1 = p1
                if c0 == c1:
                    if r0 > r1:
                        r0, r1 = r1, r0

                    for r in range(r0, r1 + 1):
                        self.grid[r][c0] = '#'
                else:
                    if c0 > c1:
                        c0, c1 = c1, c0

                    for c in range(c0, c1 + 1):
                        self.grid[r0][c] = '#'

    def print(self):
        for row in self.grid:
            print(''.join(row))

    def simulate(self, r0, c0):
        gone = '~'
        r, c = r0, c0
        while True:
            if self.grid[r][c] != '.':
                return False

            if r + 1 == self.rows:
                self.grid[r][c] = gone
                return False

            if self.grid[r + 1][c] == '.':
                r += 1
                continue

            if c - 1 < 0:
                self.grid[r][c] = gone
                return False

            if self.grid[r + 1][c - 1] == '.':
                r += 1
                c -= 1
                continue

            if c + 1 == self.cols:
                self.grid[r][c] = gone
                return False

            if self.grid[r + 1][c + 1] == '.':
                r += 1
                c += 1
                continue

            self.grid[r][c] = 'o'
            return True


def solve(lines):
    paths = parse_paths(lines)
    grid = Grid(paths)
    count = 0
    while grid.simulate(0, 500):
        count += 1

    return count


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines))


if __name__ == '__main__':
    main()

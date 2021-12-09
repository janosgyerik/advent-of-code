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


class Grid:
    def __init__(self, grid):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])

    def total_risk_level(self):
        low_points = self.low_points()
        return sum(self.grid[r][c] + 1 for r, c in low_points)

    def low_points(self):
        for r, row in enumerate(self.grid):
            for c, x in enumerate(row):
                if self.is_low_point(r, c):
                    yield r, c

    def is_low_point(self, r, c):
        for r2, c2 in (r+1, c), (r-1, c), (r, c+1), (r, c-1):
            if 0 <= r2 < self.rows and 0 <= c2 < self.cols:
                if self.grid[r2][c2] <= self.grid[r][c]:
                    return False

        return True


def parse_grid(lines):
    grid = [[int(x) for x in line] for line in lines]
    return Grid(grid)


def solve(lines):
    grid = parse_grid(lines)
    return grid.total_risk_level()


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines))


if __name__ == '__main__':
    main()

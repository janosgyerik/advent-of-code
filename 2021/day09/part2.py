#!/usr/bin/env python
import functools
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

    def total_basin_risk(self):
        basins = sorted(self.basins(), reverse=True)
        return functools.reduce(lambda x, y: x * y, basins[0:3], 1)

    def basins(self):
        for r, row in enumerate(self.grid):
            for c, x in enumerate(row):
                if self.grid[r][c] < 9:
                    yield self.fill_basin(r, c)

    def fill_basin(self, r, c):
        if not (0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c] < 9):
            return 0

        self.grid[r][c] = 9
        count = 1
        for r2, c2 in (r+1, c), (r-1, c), (r, c+1), (r, c-1):
            count += self.fill_basin(r2, c2)

        return count


def parse_grid(lines):
    grid = [[int(x) for x in line] for line in lines]
    return Grid(grid)


def solve(lines):
    grid = parse_grid(lines)
    return grid.total_basin_risk()


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines))


if __name__ == '__main__':
    main()

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


def ints(line):
    return [int(x) for x in line.split(' ')]


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


def parse_grid(lines):
    grid = []
    start = None
    end = None

    for r, row in enumerate(lines):
        grid.append([])
        for c, x in enumerate(row):
            if x == 'S':
                start = (r, c)
                x = 'a'
            elif x == 'E':
                end = (r, c)
                x = 'z'

            grid[-1].append(ord(x))

    assert start
    assert end
    return Grid(grid, start, end)


class Grid:
    def __init__(self, grid, start, end):
        self.grid = grid
        self.start = start
        self.end = end

    def find_shortest(self, start, end):
        rows = len(self.grid)
        cols = len(self.grid[0])

        seen = {start}
        q = deque([start])
        d = 0
        while q:
            for _ in range(len(q)):
                current = q.popleft()
                if current == end:
                    return d

                r, c = current
                e0 = self.grid[r][c]
                for dr, dc in (1, 0), (-1, 0), (0, 1), (0, -1):
                    r2 = r + dr
                    c2 = c + dc
                    if not (0 <= r2 < rows and 0 <= c2 < cols):
                        continue

                    if (r2, c2) in seen:
                        continue

                    e1 = self.grid[r2][c2]
                    if e1 <= e0 + 1:
                        seen.add((r2, c2))
                        q.append((r2, c2))

            d += 1

        raise ValueError('not found!')

    def print(self):
        for row in self.grid:
            print(''.join(chr(c) for c in row))


def solve(lines):
    grid = parse_grid(lines)
    grid.print()
    return grid.find_shortest(grid.start, grid.end)


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines))


if __name__ == '__main__':
    main()

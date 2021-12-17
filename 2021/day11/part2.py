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


neighbors = ((-1, 1), (-1, 0), (-1, -1), (0, 1), (0, -1), (1, 1), (1, 0), (1, -1))


class Sim:
    def __init__(self, grid):
        self.grid = grid
        self.flashes = 0
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])

    def step(self):
        for r, row in enumerate(self.grid):
            for c, _ in enumerate(row):
                self.grid[r][c] += 1

        while True:
            flashes = 0
            for r, row in enumerate(self.grid):
                for c, x in enumerate(row):
                    if self.grid[r][c] > 9:
                        flashes += 1
                        self.flash(r, c)

            if flashes == 0:
                break

    def flash(self, r, c):
        self.flashes += 1
        self.grid[r][c] = 0

        for dr, dc in neighbors:
            r2 = r + dr
            c2 = c + dc
            if not (0 <= r2 < self.rows and 0 <= c2 < self.cols and self.grid[r2][c2] > 0):
                continue

            self.grid[r2][c2] += 1

    def print(self):
        for row in self.grid:
            print(''.join(str(x) for x in row))

        print()


def line_to_grid(line):
    return [int(c) for c in line]


def lines_to_grid(lines):
    return [line_to_grid(line) for line in lines]


def solve(lines):
    sim = Sim(lines_to_grid(lines))

    prev = 0
    for step in range(1, 1000):
        sim.step()
        if sim.flashes - prev == 100:
            return step

        prev = sim.flashes


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines))


if __name__ == '__main__':
    main()

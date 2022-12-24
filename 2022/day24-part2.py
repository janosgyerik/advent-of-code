#!/usr/bin/env python
import functools
import re
import sys
from collections import namedtuple, Counter, deque, defaultdict
from dataclasses import dataclass, field
from functools import lru_cache
from heapq import heappush, heappop, heapify
from itertools import product
from typing import Callable, List, Set, Tuple, Dict

from utils.binary_search import binary_search
from utils import parsing
from utils import coordinates
from enum import Enum, auto
from utils import grids


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


def parse_and_solve(lines, *args):
    input_ = parse_input(lines)
    return solve(input_)


def main():
    lines = read_lines(sys.argv[1])
    print(parse_and_solve(lines, *(sys.argv[2:])))


DRCS = {
    '>': (0, 1),
    '<': (0, -1),
    'v': (1, 0),
    '^': (-1, 0),
}


@dataclass
class Blizzard:
    r: int
    c: int
    label: str


@dataclass
class Blizzards:
    blizzards: List[Blizzard]
    bottom: int
    right: int
    positions: Set[Tuple[int, int]] = field(init=False)

    def __post_init__(self):
        self.positions = set()

    def simulate(self):
        self.positions.clear()

        for b in self.blizzards:
            dr, dc = DRCS[b.label]
            r = b.r + dr
            c = b.c + dc
            if r == 0:
                r = self.bottom - 1
            elif r == self.bottom:
                r = 1
            elif c == 0:
                c = self.right - 1
            elif c == self.right:
                c = 1

            b.r = r
            b.c = c
            self.positions.add((r, c))

    def is_clear(self, r, c):
        return (r, c) not in self.positions


@dataclass
class Valley:
    grid: grids.Grid
    blizzards: Blizzards = field(init=False)
    start: Tuple[int, int] = field(init=False)
    end: Tuple[int, int] = field(init=False)
    empty_grid: grids.Grid = field(init=False)

    def __post_init__(self):
        self.empty_grid = self.grid.copy()
        for r in range(1, self.grid.rows - 1):
            for c in range(1, self.grid.cols - 1):
                self.empty_grid[r][c] = '.'

        self.start = 0, 1
        self.end = self.grid.rows - 1, self.grid.cols - 2
        assert self.grid[self.start[0]][self.start[1]] == '.'
        assert self.grid[self.end[0]][self.end[1]] == '.'

        blizzards = []

        for r, row in enumerate(self.grid):
            for c, x in enumerate(row):
                if x in '<>v^':
                    blizzards.append(Blizzard(r, c, x))

        self.blizzards = Blizzards(blizzards, self.grid.rows - 1, self.grid.cols - 1)

    def print(self, candidates):
        grid = self.empty_grid.copy()

        for b in self.blizzards.blizzards:
            r, c = b.r, b.c
            if grid[r][c] == '.':
                grid[r][c] = b.label
            elif '2' <= grid[r][c] <= '5':
                grid[r][c] = str(chr(ord(grid[r][c]) + 1))
            else:
                grid[r][c] = '2'

        for r, c in candidates:
            if grid[r][c] != '.':
                grid.print()
                raise ValueError(f'position ({r}, {c}) was expected empty; verify candidates={candidates}')

            grid[r][c] = 'E'

        grid.print()
        print()

    def shortest_path_out(self, start, end):
        q = {start}
        for step in range(1, 2000):
            self.blizzards.simulate()
            q2 = set()
            for r, c in q:
                if self.blizzards.is_clear(r, c):
                    q2.add((r, c))

                for r2, c2 in coordinates.neighbors(r, c):
                    if (r2, c2) == end:
                        return step

                    if not (0 < r2 < self.grid.rows - 1 and 0 < c2 < self.grid.cols - 1):
                        continue

                    if not self.blizzards.is_clear(r2, c2):
                        # print(f'not clear in ({r2}, {c2})')
                        # print(self.blizzards.positions)
                        # print((r2, c2) not in self.blizzards.positions)
                        continue

                    q2.add((r2, c2))

            q = q2
            # self.print(q)

        return -1


@dataclass
class Input:
    lines: List[str]
    valley: Valley


def parse_input(lines):
    grid = [[c for c in line] for line in lines]
    grid = grids.Grid(grid)

    return Input(lines, Valley(grid))


def solve(input_):
    # input_.valley.print()
    # input_.valley.simulate(3)
    valley = input_.valley
    first = valley.shortest_path_out(valley.start, valley.end)
    back = valley.shortest_path_out(valley.end, valley.start)
    second = valley.shortest_path_out(valley.start, valley.end)
    return first, back, second, sum([first, back, second])


if __name__ == '__main__':
    main()

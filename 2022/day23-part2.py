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


@dataclass
class Input:
    lines: List[str]
    grid: grids.Grid


def parse_input(lines):
    grid = grids.Grid([[c for c in line] for line in lines])
    return Input(lines, grid)


@dataclass
class Elves:
    grid: grids.Grid
    drs: deque[Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]] = field(init=False)
    elves: Set[Tuple[int, int]] = field(init=False)
    min_r: int = 0
    max_r: int = 0
    min_c: int = 0
    max_c: int = 0

    def __post_init__(self):
        self.drs = deque([
            # north
            ((-1, -1), (-1, 0), (-1, 1)),
            # south
            ((1, -1), (1, 0), (1, 1)),
            # west
            ((-1, -1), (0, -1), (1, -1)),
            # east
            ((-1, 1), (0, 1), (1, 1)),
        ])
        
        self.elves = elves = set()
        for r, row in enumerate(self.grid):
            for c, x in enumerate(row):
                if x == '#':
                    elves.add((r, c))
                    self.max_r = max(self.max_r, r)
                    self.max_c = max(self.max_c, c)

    def simulate(self):
        moves = self._compute_moves()
        self._apply_moves(moves)
        self.drs.rotate(-1)

        return any(elf != target for elf, target in moves.items())

    def _compute_moves(self):
        moves = {}
        for elf in self.elves:
            r, c = elf
            for dr, dc in coordinates.neighbors_all(r, c):
                elf2 = r + dr, c + dc
                if elf2 in self.elves:
                    break
            else:
                moves[elf] = elf
                continue

            for drs in self.drs:
                for dr, dc in drs:
                    target = r + dr, c + dc
                    if target in self.elves:
                        break
            
                else:
                    dr, dc = drs[1]
                    target = r + dr, c + dc
                    moves[elf] = target
                    break
            else:
                moves[elf] = elf
                continue

        assert len(moves) == len(self.elves)
        return moves

    def _apply_moves(self, moves):
        collisions = set()
        seen = set()
        for target in moves.values():
            if target in seen:
                collisions.add(target)
            seen.add(target)
            
        elves = set()
        for elf, target in moves.items():
            if elf == target or target in collisions:
                elves.add(elf)
            else:
                elves.add(target)
                r, c = target
                self.min_r = min(self.min_r, r)
                self.max_r = max(self.max_r, r)
                self.min_c = min(self.min_c, c)
                self.max_c = max(self.max_c, c)

        assert len(elves) == len(self.elves)
        self.elves = elves

    def count_empty(self):
        rows = self.max_r - self.min_r + 1
        cols = self.max_c - self.min_c + 1
        return rows * cols - len(self.elves)

    def print(self):
        rows = self.max_r - self.min_r + 1
        cols = self.max_c - self.min_c + 1
        grid = [['.'] * cols for _ in range(rows)]
        for r, c in self.elves:
            r2 = r - self.min_r
            c2 = c - self.min_c
            grid[r2][c2] = '#'
        grids.Grid(grid).print()
        print()


def solve(input_):
    grid = input_.grid
    # grid.print()

    elves = Elves(grid)
    # elves.print()

    count = 1
    while elves.simulate():
        count += 1

    return count


if __name__ == '__main__':
    main()

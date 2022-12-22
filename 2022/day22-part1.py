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


@dataclass
class Board:
    grid: grids.Grid

    def find_start(self):
        for r, row in enumerate(self.grid):
            for c, x in enumerate(row):
                if x == '.':
                    return r, c

    def move(self, start_pos, path):
        r, c = start_pos
        facings = deque([(0, 1), (1, 0), (0, -1), (-1, 0)])

        for p in path:
            if isinstance(p, int):
                for _ in range(p):
                    dr, dc = facings[0]
                    r2 = r + dr
                    c2 = c + dc

                    while True:
                        if r2 == self.grid.rows:
                            r2 = 0
                        elif r2 == -1:
                            r2 = self.grid.rows - 1
                        elif c2 == self.grid.cols:
                            c2 = 0
                        elif c2 == -1:
                            c2 = self.grid.cols - 1

                        if self.grid[r2][c2] == ' ':
                            r2 += dr
                            c2 += dc
                        else:
                            break

                    if self.grid[r2][c2] == '.':
                        r, c = r2, c2
                    else:
                        break

            elif p == 'L':
                facings.rotate(1)

            else:
                facings.rotate(-1)

        return r, c, facings[0]


def parse_int(s, index):
    length = 0
    steps = 0
    while index < len(s) and '0' <= s[index] <= '9':
        steps *= 10
        steps += int(s[index])
        index += 1
        length += 1

    return steps, length


def parse_input(lines):
    grid = []
    for line in lines:
        if not line:
            break

        grid.append(line)

    width = max(len(row) for row in grid)
    for r, row in enumerate(grid):
        if len(row) < width:
            grid[r] += ' ' * (width - len(row))

    board = Board(grids.Grid(grid))

    path_str = lines[-1]
    path = []
    index = 0
    while True:
        steps, length = parse_int(path_str, index)
        path.append(steps)

        index += length
        if index == len(path_str):
            break

        direction = path_str[index]
        index += 1
        path.append(direction)

    return board, path


def solve(lines, *args):
    board, path = parse_input(lines)
    print(path)
    start = board.find_start()
    r, c, facing = board.move(start, path)
    print(r, c, facing)

    facings = {
        (0, 1): 0,
        (1, 0): 1,
        (0, -1): 2,
        (-1, 0): 3,
    }
    return (r + 1) * 1000 + 4 * (c + 1) + facings[facing]


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines, *(sys.argv[2:])))


if __name__ == '__main__':
    main()

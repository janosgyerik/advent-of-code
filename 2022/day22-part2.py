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
    subgrids: List[grids.Grid] = field(init=False)
    transitions: Dict[int, Dict[Tuple[int, int], Tuple[grids.Grid, Callable]]] = field(init=False)

    def __post_init__(self):
        dim = self.grid.rows // 4
        # dim = self.grid.rows // 3

        m = dim - 1
        left = 0, -1
        right = 0, 1
        up = -1, 0
        down = 1, 0

        transitions = {
            'BT': lambda r, c: (0, c, down),
            'TB': lambda r, c: (m, c, up),
            'RL': lambda r, c: (r, 0, right),
            'LR': lambda r, c: (r, m, left),
            'BR': lambda r, c: (c, m, left),
            'RB': lambda r, c: (m, r, up),
            'LT': lambda r, c: (0, r, down),
            'TL': lambda r, c: (c, 0, right),
            'RR': lambda r, c: (m - r, m, left),
            'LL': lambda r, c: (m - r, 0, right),
            'TT': lambda r, c: (0, m - c, down),
            'BB': lambda r, c: (m, m - c, up),
            'LB': lambda r, c: (m, m - r, up),
            'BL': lambda r, c: (m - c, 0, right),
            'RT': lambda r, c: (0, m - r, down),
            'TR': lambda r, c: (m - c, m, left),
        }

        g1 = self._subgrid(1, dim, 3, 0)
        g2 = self._subgrid(2, dim, 2, 0)
        g3 = self._subgrid(3, dim, 2, 1)
        g4 = self._subgrid(4, dim, 1, 1)
        g5 = self._subgrid(5, dim, 0, 1)
        g6 = self._subgrid(6, dim, 0, 2)

        # g1 = self._subgrid(1, dim, 0, 2)
        # g2 = self._subgrid(2, dim, 1, 0)
        # g3 = self._subgrid(3, dim, 1, 1)
        # g4 = self._subgrid(4, dim, 1, 2)
        # g5 = self._subgrid(5, dim, 2, 2)
        # g6 = self._subgrid(6, dim, 2, 3)

        self.subgrids = [g1, g2, g3, g4, g5, g6]

        self.transitions = {
            1: {
                left: (g5, transitions['LT']),
                down: (g6, transitions['BT']),
                right: (g3, transitions['RB']),
                up: (g2, transitions['TB']),
            },
            2: {
                left: (g5, transitions['LL']),
                down: (g1, transitions['BT']),
                right: (g3, transitions['RL']),
                up: (g4, transitions['TL']),
            },
            3: {
                left: (g2, transitions['LR']),
                down: (g1, transitions['BR']),
                right: (g6, transitions['RR']),
                up: (g4, transitions['TB']),
            },
            4: {
                left: (g2, transitions['LT']),
                down: (g3, transitions['BT']),
                right: (g6, transitions['RB']),
                up: (g5, transitions['TB']),
            },
            5: {
                left: (g2, transitions['LL']),
                down: (g4, transitions['BT']),
                right: (g6, transitions['RL']),
                up: (g1, transitions['TL']),
            },
            6: {
                left: (g5, transitions['LR']),
                down: (g4, transitions['BR']),
                right: (g3, transitions['RR']),
                up: (g1, transitions['TB']),
            },
        }

        # self.transitions = {
        #     1: {
        #         left: (g3, transitions['LT']),
        #         down: (g4, transitions['BT']),
        #         right: (g6, transitions['RR']),
        #         up: (g2, transitions['TT']),
        #     },
        #     2: {
        #         left: (g6, transitions['LB']),
        #         down: (g5, transitions['BB']),
        #         right: (g3, transitions['RL']),
        #         up: (g1, transitions['TL']),
        #     },
        #     3: {
        #         left: (g2, transitions['LR']),
        #         down: (g5, transitions['BL']),
        #         right: (g4, transitions['RL']),
        #         up: (g1, transitions['TL']),
        #     },
        #     4: {
        #         left: (g3, transitions['LR']),
        #         down: (g5, transitions['BT']),
        #         right: (g6, transitions['RT']),
        #         up: (g1, transitions['TB']),
        #     },
        #     5: {
        #         left: (g3, transitions['LB']),
        #         down: (g2, transitions['BB']),
        #         right: (g6, transitions['RL']),
        #         up: (g4, transitions['TB']),
        #     },
        #     6: {
        #         left: (g5, transitions['LR']),
        #         down: (g2, transitions['BL']),
        #         right: (g1, transitions['RR']),
        #         up: (g4, transitions['TR']),
        #     },
        # }

    def _subgrid(self, id_, dim, r2, c2) -> grids.Grid:
        base_r = dim * r2
        base_c = dim * c2

        grid = [[None] * dim for _ in range(dim)]
        for r in range(dim):
            r3 = base_r + r
            for c in range(dim):
                c3 = base_c + c
                grid[r][c] = self.grid[r3][c3], id_, r3, c3

        return grids.Grid(grid)

    def find_start(self):
        for r, row in enumerate(self.grid):
            for c, x in enumerate(row):
                if x == '.':
                    return r, c

    def move(self, path):
        r, c = 0, 0
        facings = deque([(0, 1), (1, 0), (0, -1), (-1, 0)])
        grid = self.subgrids[4]
        # grid = self.subgrids[0]

        dirs = {
            (0, 1): '>',
            (0, -1): '<',
            (1, 0): 'v',
            (-1, 0): '^',
        }

        for p in path:
            if p == 'L':
                facings.rotate(1)

            elif p == 'R':
                facings.rotate(-1)

            else:
                for _ in range(p):
                    facing = facings[0]
                    dr, dc = facing
                    r2 = r + dr
                    c2 = c + dc

                    if 0 <= r2 < grid.rows and 0 <= c2 < grid.cols:
                        if grid[r2][c2][0] == '#':
                            break

                        r, c = r2, c2

                    else:
                        _, grid_id, _, _ = grid[r][c]
                        grid2, transition = self.transitions[grid_id][facing]
                        # print(r2, c2, facing, grid_id, grid2[0][0][1])
                        r2, c2, facing2 = transition(r2, c2)
                        # print(r2, c2, facing2)
                        if grid2[r2][c2][0] == '#':
                            break
                        else:
                            grid, r, c = grid2, r2, c2
                            while facings[0] != facing2:
                                facings.rotate(1)
                                facing = facings[0]

                    x, _, r3, c3 = grid[r][c]
                    assert x in '.#'
                    self.grid[r3][c3] = dirs[facing]
                    # self.grid.print()

        _, _, r0, c0 = grid[r][c]
        return r0, c0, facings[0]


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
    r, c, facing = board.move(path)
    print(r, c, facing)

    facings = {
        (0, 1): 0,
        (1, 0): 1,
        (0, -1): 2,
        (-1, 0): 3,
    }
    return 1000 * (r + 1) + 4 * (c + 1) + facings[facing]


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines, *(sys.argv[2:])))


if __name__ == '__main__':
    main()

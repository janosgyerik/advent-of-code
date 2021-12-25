#!/usr/bin/env python
import math
from numbers import Number
from typing import Callable, Any

import utils
import re
from collections import namedtuple, Counter, deque, defaultdict
from itertools import product
from heapq import heappush, heappop, heapify
from functools import lru_cache
import utils


def parse_cucumbers(lines):
    rows = len(lines)
    cols = len(lines[0])
    east_facing = set()
    south_facing = set()

    for r, line in enumerate(lines):
        for c, x in enumerate(line):
            if x == '>':
                east_facing.add((r, c))
            elif x == 'v':
                south_facing.add((r, c))

    return Cucumbers(rows, cols, east_facing, south_facing)


class Cucumbers:
    def __init__(self, rows, cols, east_facing, south_facing):
        self.rows = rows
        self.cols = cols
        self.east_facing = east_facing
        self.south_facing = south_facing

    def step(self):
        def wrap(limit, value):
            if value == limit:
                return 0

            return value

        def move(flock, next_pos):
            to_move = []
            for r, c in flock:
                pos = next_pos(r, c)
                if pos not in self.east_facing and pos not in self.south_facing:
                    to_move.append(((r, c), pos))

            for old_pos, new_pos in to_move:
                flock.remove(old_pos)
                flock.add(new_pos)

            return len(to_move)

        def next_pos_east(r, c):
            return r, wrap(self.cols, c + 1)

        def next_pos_south(r, c):
            return wrap(self.rows, r + 1), c

        def move_east():
            return move(self.east_facing, next_pos_east)

        def move_south():
            return move(self.south_facing, next_pos_south)

        moved = move_east() + move_south()
        return moved > 0

    def print(self):
        for r in range(self.rows):
            for c in range(self.cols):
                pos = r, c
                if pos in self.east_facing:
                    print('>', end='')
                    assert pos not in self.south_facing
                elif pos in self.south_facing:
                    print('v', end='')
                else:
                    print('.', end='')

            print()
        print()


def solve(lines):
    cucumbers = parse_cucumbers(lines)
    for step in range(1000):
        if not cucumbers.step():
            return step + 1


if __name__ == '__main__':
    utils.solve(solve)

#!/usr/bin/env python
import functools
import re
import sys
from collections import namedtuple, Counter, deque, defaultdict
from dataclasses import dataclass, field
from functools import lru_cache
from heapq import heappush, heappop, heapify
from itertools import product
from typing import Callable, List, Set, Tuple

from utils.binary_search import binary_search
from utils import parsing


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


def manhattan_distance(sx, sy, bx, by):
    return abs(sx - bx) + abs(sy - by)


@dataclass
class Cubes:
    cubes: Set[Tuple[int, int, int]]
    min_x: int = field(init=False)
    min_y: int = field(init=False)
    min_z: int = field(init=False)
    max_x: int = field(init=False)
    max_y: int = field(init=False)
    max_z: int = field(init=False)

    def __post_init__(self):
        self.min_x = min(q[0] for q in self.cubes) - 1
        self.min_y = min(q[1] for q in self.cubes) - 1
        self.min_z = min(q[2] for q in self.cubes) - 1
        self.max_x = max(q[0] for q in self.cubes) + 1
        self.max_y = max(q[1] for q in self.cubes) + 1
        self.max_z = max(q[2] for q in self.cubes) + 1

    def count_open_surfaces(self):
        enclosure = self._compute_enclosure()

        count = 0
        for x, y, z in self.cubes:
            for dx, dy, dz in DIRS:
                v = x + dx, y + dy, z + dz
                if v in enclosure:
                    count += 1

        return count

    def _compute_enclosure(self):
        filled = set()

        stack = [(self.min_x, self.min_y, self.min_z)]
        while stack:
            x, y, z = stack.pop()
            u = x, y, z
            if u in filled or u in self.cubes:
                continue

            if not (self.min_x <= x <= self.max_x
                    and self.min_y <= y <= self.max_y
                    and self.min_z <= z <= self.max_z):
                continue

            filled.add(u)
            for dx, dy, dz in DIRS:
                stack.append((x + dx, y + dy, z + dz))

        return filled


DIRS = ((0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0))


def parse_cubes(lines):
    cubes = set()
    for line in lines:
        x, y, z = parsing.extract_natural_numbers(line)
        cubes.add((x, y, z))

    return Cubes(cubes)


def solve(lines, *args):
    cubes = parse_cubes(lines)
    return cubes.count_open_surfaces()


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines, *(sys.argv[2:])))


if __name__ == '__main__':
    main()

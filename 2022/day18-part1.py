#!/usr/bin/env python
import functools
import re
import sys
from collections import namedtuple, Counter, deque, defaultdict
from dataclasses import dataclass, field
from functools import lru_cache
from heapq import heappush, heappop, heapify
from itertools import product
from typing import Callable, List

from utils.binary_search import binary_search
from utils import parsing


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


def manhattan_distance(sx, sy, bx, by):
    return abs(sx - bx) + abs(sy - by)


@dataclass
class Cube:
    x: int
    y: int
    z: int


class Graph:
    def __init__(self):
        self.neighbors = defaultdict(set)

    def connect(self, u, v):
        self.neighbors[u].add(v)
        self.neighbors[v].add(u)

    def count_open_surfaces(self):
        count = 0
        for u, vs in self.neighbors.items():
            count += 6 - len(vs)
        return count

    def add(self, u):
        self.neighbors[u] = set()


DIRS = ((0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0))


def parse_cubes(lines):
    cubes = []
    for line in lines:
        x, y, z = parsing.extract_natural_numbers(line)
        # cube = Cube(x, y, z)
        # print(cube)
        cubes.append((x, y, z))

    coords = set()
    for x, y, z in cubes:
        coords.add((x, y, z))

    g = Graph()
    for u in cubes:
        x, y, z = u
        g.add(u)
        for dx, dy, dz in DIRS:
            v = x + dx, y + dy, z + dz
            if v in cubes:
                g.connect(u, v)

    return g


def solve(lines, *args):
    g = parse_cubes(lines)
    return g.count_open_surfaces()


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines, *(sys.argv[2:])))


if __name__ == '__main__':
    main()

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

    def count_inner_surfaces(self, inner):
        count = 0
        for x, y, z in self.neighbors:
            for dx, dy, dz in DIRS:
                v = x + dx, y + dy, z + dz
                if v in inner:
                    count += 1

        return count

    def add(self, u):
        self.neighbors[u] = set()

    def compute_bounds(self):
        pivot = next(u for u in self.neighbors)
        min_x, min_y, min_z = pivot
        max_x, max_y, max_z = pivot
        for x, y, z in self.neighbors:
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            min_z = min(min_z, z)
            max_x = max(max_x, x)
            max_y = max(max_y, y)
            max_z = max(max_z, z)

        return min_x - 1, min_y - 1, min_z - 1, max_x + 1, max_y + 1, max_z + 1

    def fill(self, bounds):
        min_x, min_y, min_z, max_x, max_y, max_z = bounds
        filled = set()

        def fill(x, y, z):
            u = x, y, z
            if u in filled or u in self.neighbors:
                return

            if not (min_x <= x <= max_x and min_y <= y <= max_y and min_z <= z <= max_z):
                return

            filled.add(u)
            for dx, dy, dz in DIRS:
                v = x + dx, y + dy, z + dz
                fill(*v)

        fill(min_x, min_y, min_z)

        return filled

    def find_innner(self, bounds, filled):
        min_x, min_y, min_z, max_x, max_y, max_z = bounds
        inner = set()

        for x in range(min_x, max_x):
            for y in range(min_y, max_y):
                for z in range(min_z, max_z):
                    u = x, y, z
                    if u not in filled and u not in self.neighbors:
                        inner.add(u)

        return inner


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
    bounds = g.compute_bounds()
    print(sys.getrecursionlimit())
    sys.setrecursionlimit(15000)

    filled = g.fill(bounds)
    print(len(filled))

    inner = g.find_innner(bounds, filled)
    print(len(inner))

    return g.count_open_surfaces() - g.count_inner_surfaces(inner)


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines, *(sys.argv[2:])))


if __name__ == '__main__':
    main()

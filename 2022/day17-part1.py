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


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


def manhattan_distance(sx, sy, bx, by):
    return abs(sx - bx) + abs(sy - by)


class Jets:
    def __init__(self, jets):
        dx = {
            '<': -1,
            '>': 1,
        }
        self.jets = deque(dx[c] for c in jets)

    def next(self):
        self.jets.rotate(-1)
        return self.jets[-1]


class Shape:
    def __init__(self, rows):
        self.rows = rows

    def height(self):
        return len(self.rows)


class Shapes:
    def __init__(self):
        self.shapes = deque([
            Shape(['####']),
            Shape([' # ', '###', ' # ']),
            Shape(['  #', '  #', '###']),
            Shape(['#', '#', '#', '#']),
            Shape(['##', '##']),
        ])

    def next(self):
        self.shapes.rotate(-1)
        return self.shapes[-1]


class Rock:
    def __init__(self, shape, x, y):
        self.rows = shape.rows
        self.x = x
        self.y = y

    def coordinates(self):
        coordinates = []
        for r, row in enumerate(self.rows):
            for c, x in enumerate(row):
                if x == '#':
                    coordinates.append((self.x + c, self.y - r))

        return sorted(coordinates, key=lambda z: z[1])

    def __str__(self):
        return '\n'.join(self.rows)


class Chamber:
    def __init__(self, width, startcol, jets):
        self.width = width
        self.startcol = startcol
        self.jets = jets
        self.shapes = Shapes()
        self.chamber = deque()

    def height(self):
        return len(self.chamber)

    def simulate(self, count):
        for _ in range(count):
            shape = self.shapes.next()
            rock = Rock(shape, 2, self.height() + 3 + shape.height() - 1)
            while True:
                dx = self.jets.next()
                self.tryshift(rock, dx)
                if not self.tryfall(rock):
                    self.add(rock)
                    break

    def add(self, rock):
        for x, y in rock.coordinates():
            if self.height() == y:
                self.chamber.append(['.'] * self.width)
            self.chamber[y][x] = '#'

    def tryshift(self, rock, dx):
        for x, y in rock.coordinates():
            x += dx
            if not (0 <= x < self.width):
                return False

            if self.height() <= y:
                continue

            if self.chamber[y][x] == '#':
                return False

        rock.x += dx
        return True

    def tryfall(self, rock):
        for x, y in rock.coordinates():
            y -= 1
            if self.height() <= y:
                continue

            if y < 0 or self.chamber[y][x] == '#':
                return False

        rock.y -= 1
        return True

    def print(self):
        for row in reversed(self.chamber):
            print(''.join(row))

        print()


def solve(lines, count, *args):
    count = int(count)
    jets = Jets(lines[0])
    chamber = Chamber(7, 2, jets)
    chamber.simulate(count)
    if args:
        chamber.print()
    return chamber.height()


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines, *(sys.argv[2:])))


if __name__ == '__main__':
    main()

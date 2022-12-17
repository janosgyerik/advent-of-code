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
        self.chamber = []
        self.eliminated_height = 0

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
                    self.simplify()
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
        w = len(str(self.height()))
        for index, row in reversed(list(enumerate(self.chamber))):
            print(f"{index: <{w}}", ''.join(row))

        print()

    def simplify(self):
        if self._is_full_row(self.height() - 1):
            print('full row found!')
            return
        if self._is_full_row(self.height() - 2):
            print('full row found! at - 2')
            return
        if self._is_full_row(self.height() - 3):
            print('full row found! at - 2')
            return
        return
        for r, c, targetc, dc in (
                (self.height() - 1, 0, self.width, 1),
                (self.height() - 2, 0, self.width, 1),
                (self.height() - 1, self.width - 1, -1, -1),
                (self.height() - 2, self.width - 1, -1, -1),
        ):
            if r := self._can_seal(r, c, targetc, dc):
                self.chamber[:r - 1] = []
                self.eliminated_height += r - 1
                return

    def _can_seal(self, r, c, targetc, dc):
        if c == targetc:
            return r

        if r < 0 or self.chamber[r][c] != '#':
            return False

        c += dc
        return (
                self._can_seal(r, c, targetc, dc)
                or self._can_seal(r - 1, c, targetc, dc)
                or self._can_seal(r - 1, c - dc, targetc, dc))

    def total_height(self):
        return self.eliminated_height + self.height()


def solve(lines, count, *args):
    count = int(count)
    jets = Jets(lines[0])
    chamber = Chamber(7, 2, jets)
    chamber.simulate(count)
    if args:
        chamber.print()
    return chamber.total_height()


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines, *(sys.argv[2:])))


if __name__ == '__main__':
    main()

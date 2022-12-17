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
        self.jets = deque(c == '<' for c in jets)
        for c in jets:
            if c == '<':
                pass
            elif c == '>':
                pass
            else:
                raise ValueError(f"unexpected char: {c}")
        self.count = 0

    def next(self):
        self.count += 1
        # print(self.count)
        self.jets.rotate(-1)
        return self.jets[-1]


def to_bits(row):
    bits = 0
    for c in row:
        bits <<= 1
        if c == '#':
            bits |= 1

    return bits


class Shape:
    def __init__(self, rows, width, startcol):
        shift = width - (startcol + len(rows[0]))
        self.rows = [to_bits(row) << shift for row in rows]

    def height(self):
        return len(self.rows)


class Shapes:
    def __init__(self, width, startcol):
        self.shapes = deque([
            Shape(['####'], width, startcol),
            Shape([' # ', '###', ' # '], width, startcol),
            Shape(['  #', '  #', '###'], width, startcol),
            Shape(['#', '#', '#', '#'], width, startcol),
            Shape(['##', '##'], width, startcol),
        ])

    def next(self):
        self.shapes.rotate(-1)
        return self.shapes[-1]


class Rock:
    def __init__(self, shape, y):
        self.rows = shape.rows.copy()
        self.y = y

    def coordinates(self):
        coordinates = []
        for r, row in enumerate(self.rows):
            coordinates.append((row, self.y - r))

        return reversed(coordinates)

    def shift(self, left):
        if left:
            for i, row in enumerate(self.rows):
                self.rows[i] = row << 1
        else:
            for i, row in enumerate(self.rows):
                self.rows[i] = row >> 1

    def __str__(self):
        return '\n'.join(to_chars(row, 7) for row in self.rows)


def to_chars(bits, width):
    chars = []
    while bits:
        if bits & 1:
            chars.append('#')
        else:
            chars.append('.')
        bits >>= 1

    while len(chars) < width:
        chars.append('.')

    return ''.join(reversed(chars))


class Chamber:
    def __init__(self, width, startcol, jets):
        self.width = width
        self.jets = jets
        self.shapes = Shapes(width, startcol)
        self.chamber = deque()
        self.full_row = (1 << width) - 1

    def height(self):
        return len(self.chamber)

    def simulate(self, count):
        for _ in range(count):
            shape = self.shapes.next()
            rock = Rock(shape, self.height() + 3 + shape.height() - 1)
            while True:
                left = self.jets.next()
                self.tryshift(rock, left)
                if not self.tryfall(rock):
                    self.add(rock)
                    break

    def add(self, rock):
        for bits, y in rock.coordinates():
            if self.height() == y:
                self.chamber.append(0)
            self.chamber[y] |= bits

    def tryshift(self, rock, left):
        for bits, y in rock.coordinates():
            if left:
                bits2 = bits << 1
                if bits2 > self.full_row:
                    return False
            else:
                if bits & 1:
                    return False
                bits2 = bits >> 1

            if self.height() <= y:
                continue

            if self.chamber[y] & bits2:
                return False

        rock.shift(left)
        return True

    def tryfall(self, rock):
        for bits, y in rock.coordinates():
            y -= 1
            if self.height() <= y:
                continue

            if y < 0 or (self.chamber[y] & bits):
                return False

        rock.y -= 1
        return True

    def print(self):
        for row in reversed(self.chamber):
            print(to_chars(row, self.width))

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

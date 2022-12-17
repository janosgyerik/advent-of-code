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
        self.width = len(rows[0])
        self.height = len(rows)

        shift = width - (startcol + self.width)
        self.rows = [to_bits(row) << shift for row in rows]

        value = 0
        for row in self.rows:
            value <<= 8
            value |= row
        self.value = value

        self.left = self
        self.right = self

    def shift(self, left):
        if left:
            return self.left
        return self.right

    def __str__(self):
        return '\n'.join(to_chars(row, 7) for row in self.rows)


def create_shape(rows, width, startcol):
    base = Shape(rows, width, startcol)

    prev = base
    for col in range(startcol + 1, width - base.width + 1):
        shape = Shape(rows, width, col)
        prev.right = shape
        shape.left = prev
        prev = shape

    next_ = base
    for col in range(startcol - 1, -1, -1):
        shape = Shape(rows, width, col)
        next_.left = shape
        shape.right = next_
        next_ = shape

    return base


class Shapes:
    def __init__(self, width, startcol):
        self.shapes = deque([
            create_shape(['####'], width, startcol),
            create_shape([' # ', '###', ' # '], width, startcol),
            create_shape(['  #', '  #', '###'], width, startcol),
            create_shape(['#', '#', '#', '#'], width, startcol),
            create_shape(['##', '##'], width, startcol),
        ])

    def next(self):
        self.shapes.rotate(-1)
        return self.shapes[-1]


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


class Segment:
    def __init__(self, chamber, height):
        self.mask = (1 << 8 * height) - 1
        self.index = chamber.height() - 1
        self.chamber = chamber.chamber
        self.value = 0

    def shiftdown(self):
        self.value = (self.value << 8) & self.mask
        self.value |= self.chamber[self.index]
        self.index -= 1


class Chamber:
    def __init__(self, width, startcol, jets):
        self.width = width
        self.jets = jets
        self.shapes = Shapes(width, startcol)
        self.chamber = deque([(1 << 8) - 1])
        self.full_row = (1 << width) - 1

    def height(self):
        return len(self.chamber)

    def simulate(self, count):
        for _ in range(count):
            shape = self.shapes.next()
            for _ in range(3):
                left = self.jets.next()
                shape = shape.shift(left)

            segment = Segment(self, shape.height)
            while True:
                left = self.jets.next()
                shape = self.tryshift(shape, left, segment)
                segment.shiftdown()
                if not self.tryfall(shape, segment):
                    self.add(shape, segment)
                    break

    def add(self, shape, segment):
        for i, row in reversed(list(enumerate(shape.rows))):
            chamber_index = segment.index + 2 + (shape.height - i - 1)
            if chamber_index >= self.height():
                self.chamber.append(row)
            else:
                self.chamber[chamber_index] |= row

    def tryshift(self, shape, left, segment):
        assert (shape.value & segment.value) == 0, (shape.value, segment.value)

        shifted = shape.shift(left)
        if shifted == shape:
            return shape

        if shifted.value & segment.value:
            return shape

        return shifted

    def tryfall(self, shape, segment):
        return (shape.value & segment.value) == 0

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
    return chamber.height() - 1


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines, *(sys.argv[2:])))


if __name__ == '__main__':
    main()

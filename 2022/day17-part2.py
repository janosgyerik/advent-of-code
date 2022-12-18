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
        self.counts = defaultdict(list)

    def height(self):
        return len(self.chamber)

    def simulate(self, count):
        for i in range(count):
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
                    self.counts[self.height()].append(i)
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


def find_repeated_segment(chamber, nums):
    pivot = nums[-1]
    positions = []
    for index, num in enumerate(nums):
        if num == pivot:
            positions.append(index)

    last_index = positions[-1]
    assert nums[last_index] == pivot

    for index in reversed(positions[:-2]):
        cycle_length = last_index - index
        prev_start = index - cycle_length
        for offset in range(cycle_length):
            if nums[prev_start + offset] != nums[index + offset]:
                break
        else:
            print(f'found cycle of length={cycle_length}')
            print(chamber.counts[index-1])
            print(chamber.counts[index-1 - cycle_length])
            print(chamber.counts[index-1 - cycle_length * 2])
            print(chamber.counts[index - cycle_length * 3])
            print(chamber.counts[index - cycle_length * 4])
            return cycle_length

    print(f'did not find cycle')

    return
    counts = Counter()
    for num in nums:
        counts[num] += 1

    for v, count in counts.items():
        print(v, count)


def find_count_diff(chamber, cycle_length):
    index = chamber.height() - 1
    for offset in range(5):
        if chamber.counts[index - offset]:
            index -= offset
            break
    else:
        raise ValueError("could not find count diff")

    count_diff = chamber.counts[index][-1] - chamber.counts[index - cycle_length][-1]
    print(f"found count diff = {count_diff}")

    return count_diff


def solve(lines, count1, count2, *args):
    count1 = int(count1)
    count2 = int(count2)
    jets = Jets(lines[0])
    chamber = Chamber(7, 2, jets)
    chamber.simulate(count1)
    cycle_length = find_repeated_segment(chamber, chamber.chamber)
    count_diff = find_count_diff(chamber, cycle_length)
    height = chamber.height() - 1
    height += cycle_length * ((count2 - count1) // count_diff - 1)
    count = count2 - count1 - ((count2 - count1) // count_diff - 1) * count_diff

    height0 = chamber.height()
    chamber.simulate(count)
    height += chamber.height() - height0

    if args:
        chamber.print()
    return height


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines, *(sys.argv[2:])))


if __name__ == '__main__':
    main()

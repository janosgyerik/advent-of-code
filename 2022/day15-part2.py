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


@dataclass
class Sensor:
    sx: int
    sy: int
    bx: int
    by: int
    md: int = field(init=False)

    def __post_init__(self):
        self.md = manhattan_distance(self.sx, self.sy, self.bx, self.by)

    def range_x(self, y):
        if self.sy + self.md < y:
            return None

        if y < self.sy - self.md:
            return None

        min_x = self.sx - (self.md - abs(y - self.sy))
        assert (self.md == manhattan_distance(self.sx, self.sy, min_x, y))

        max_x = self.sx + self.md - abs(y - self.sy)
        assert (self.md == manhattan_distance(self.sx, self.sy, max_x, y))

        return min_x, max_x


@dataclass
class Sensors:
    sensors: List[Sensor]

    def __post_init__(self):
        self.sensors = sorted(self.sensors, key=lambda s: s.sx)

    def find_uncovered(self, mxy):
        for y in range(mxy):
            if y % 100000 == 0:
                print(y)
            x = 0
            for s in self.sensors:
                r = s.range_x(y)
                if r is not None:
                    min_x, max_x = r
                    if min_x <= x < max_x:
                        x = max_x + 1

            if x <= mxy:
                return x, y


def parse_sensors(lines):
    template = re.compile(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)')
    sensors = []
    for line in lines:
        m = template.match(line)
        sensor = Sensor(*[int(x) for x in m.groups()])
        sensors.append(sensor)

    return Sensors(sensors)


def solve(lines, mxy):
    sensors = parse_sensors(lines)
    ans = sensors.find_uncovered(mxy)
    if ans:
        x, y = ans
        return x, y, x * 4000000 + y


def main():
    mxy = int(sys.argv[2])
    lines = read_lines(sys.argv[1])
    print(solve(lines, mxy))


if __name__ == '__main__':
    main()

#!/usr/bin/env python
import functools
import re
import sys
from collections import namedtuple, Counter, deque, defaultdict
from dataclasses import dataclass
from functools import lru_cache
from heapq import heappush, heappop, heapify
from itertools import product
from typing import Callable, List

from utils.binary_search import binary_search


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


@dataclass
class Sensor:
    sx: int
    sy: int
    bx: int
    by: int
    md: int

    def in_range(self, px, py):
        return manhattan_distance(self.sx, self.sy, px, py) <= self.md


class Sensors:
    def __init__(self, sensors):
        self.sensors = [Sensor(sx, sy, bx, by, md) for sx, sy, bx, by, md in sensors]
        self.beacons = set()
        self.min_x = 0
        self.min_y = 0
        self.max_x = 0
        self.max_y = 0
        for sx, sy, bx, by, md in sensors:
            self.beacons.add((bx, by))
            self.min_x = min(self.min_x, sx - md)
            self.min_y = min(self.min_y, sy - md)
            self.max_x = max(self.max_x, sx + md)
            self.max_y = max(self.max_y, sy + md)

        print(self.min_x, self.min_y, self.max_x, self.max_y)

    def count_covered(self, y):
        count = 0
        for x in range(self.min_x, self.max_x + 1):
            pos = (x, y)
            if pos in self.beacons:
                continue

            for i, sensor in enumerate(self.sensors):
                if sensor.in_range(*pos):
                    count += 1
                    print(i, sensor)
                    break

        return count


def manhattan_distance(sx, sy, bx, by):
    dx = abs(sx - bx)
    dy = abs(sy - by)
    return dx + dy


def parse_sensors(lines):
    re_pattern = re.compile(
        r'Sensor at x=(?P<sx>-?\d+), y=(?P<sy>-?\d+): closest beacon is at x=(?P<bx>-?\d+), y=(?P<by>-?\d+)')

    sensors = []
    for line in lines:
        m = re_pattern.match(line)
        sx, sy, bx, by = [int(m.group(x)) for x in ['sx', 'sy', 'bx', 'by']]
        md = manhattan_distance(sx, sy, bx, by)
        sensors.append([sx, sy, bx, by, md])

    return Sensors(sensors)


def solve(lines):
    sensors = parse_sensors(lines)
    y = int(sys.argv[2])
    return sensors.count_covered(y)


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines))


if __name__ == '__main__':
    main()

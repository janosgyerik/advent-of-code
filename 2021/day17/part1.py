#!/usr/bin/env python
import re
import sys
from collections import namedtuple, Counter, deque, defaultdict
from itertools import product
from heapq import heappush, heappop, heapify
from functools import lru_cache
from typing import List

import utils


class TargetArea:
    def __init__(self, x1, x2, y1, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.x_candidates = []

    def compute_x_candidates(self):
        x = 0
        while True:
            z = x * (x + 1) // 2
            if self.x1 <= z:
                break

            x += 1

        self.x_candidates.append(x)
        x += 1

        while True:
            z = x * (x + 1) // 2
            if self.x2 < z:
                break

            self.x_candidates.append(x)
            x += 1

    def highest(self):
        y = -self.y1
        while not self.can_hit_y(y):
            y -= 1

        return y * (y + 1) // 2

    def can_hit_y(self, y):
        p = 0
        v = y
        steps = 0
        while p >= self.y1:
            if p <= self.y2:
                return True

            p += v
            v -= 1
            steps += 1

        return False


def parse_desc(desc):
    return sorted([int(s) for s in desc.split('=')[1].split('..')])


def parse_target_area(s):
    # target area: x=20..30, y=-10..-5
    s = s.split(': ')[1]
    xdesc, ydesc = s.split(', ')
    x1, x2 = parse_desc(xdesc)
    y1, y2 = parse_desc(ydesc)
    return TargetArea(x1, x2, y1, y2)


def solve(lines):
    ta = parse_target_area(lines[0])
    return ta.highest()


def main():
    lines = utils.read_lines(sys.argv[1])
    print(solve(lines))


if __name__ == '__main__':
    main()

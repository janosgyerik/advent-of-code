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

    def highest(self):
        y = -self.y1
        while not self.can_hit_y(y):
            y -= 1

        return y

    def count_possible(self):
        count = 0
        for x in self.x_candidates():
            count += self.count_possible_given_x(x)

        return count

    def x_candidates(self):
        for x in range(self.x1, self.x2 + 1):
            yield x

        x = 0
        while x * (x + 1) // 2 < self.x1:
            x += 1

        yield x

        x += 1
        while x * (x + 1) // 2 <= self.x2:
            yield x
            x += 1

        while self.can_hit_x(x):
            yield x
            x += 1

        while x < self.x1:
            yield x
            x += 1

    def count_possible_given_x(self, x):
        count = 0
        for y in range(self.y1, self.highest() + 1):
            if self.can_hit(x, y):
                count += 1

        return count

    def can_hit_x(self, vx):
        p = 0
        while p <= self.x2:
            if self.x1 <= p:
                return True

            p += vx
            vx -= 1
            if vx < 0:
                break

        return False

    def can_hit_y(self, vy):
        p = 0
        while self.y1 <= p:
            if p <= self.y2:
                return True

            p += vy
            vy -= 1

        return False

    def can_hit(self, vx, vy):
        x = 0
        y = 0
        while x <= self.x2 and self.y1 <= y:
            if self.x1 <= x and y <= self.y2:
                return True

            x += vx
            vx -= 1
            vx = max(vx, 0)
            y += vy
            vy -= 1

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

    # in the example
    # width * height
    # x: 6 to 15
    # y: ...
    # for each candidate x, find the number of possible y
    return ta.count_possible()


def main():
    lines = utils.read_lines(sys.argv[1])
    print(solve(lines))


if __name__ == '__main__':
    main()

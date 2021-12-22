#!/usr/bin/env python
import math

import utils
import re
from collections import namedtuple, Counter, deque, defaultdict
from itertools import product
from heapq import heappush, heappop, heapify
from functools import lru_cache
import utils


class Step:
    def __init__(self, on, x1, x2, y1, y2, z1, z2):
        self.on = on
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.z1 = z1
        self.z2 = z2

    def in_range(self, dim):
        return (-dim <= self.x1 <= self.x2 <= dim
                and -dim <= self.y1 <= self.y2 <= dim
                and -dim <= self.z1 <= self.z2 <= dim)


def parse_step(line):
    return Step(line.startswith('on '), *utils.extract_all_valid_ints(line))


def parse_steps(lines):
    for line in lines:
        yield parse_step(line)


class Reactor:
    def __init__(self, dim, steps):
        self.dim = dim
        self.steps = steps
        self.cuboids = defaultdict(int)

    def reboot(self):
        for step in self.steps:
            self.apply_step(step)

    def count_active_cubes(self):
        count = 0
        for x in range(-self.dim, self.dim + 1):
            for y in range(-self.dim, self.dim + 1):
                for z in range(-self.dim, self.dim + 1):
                    if self.cuboids[x, y, z]:
                        count += 1

        return count

    def apply_step(self, step):
        if not step.in_range(self.dim):
            return

        for x in range(step.x1, step.x2 + 1):
            for y in range(step.y1, step.y2 + 1):
                for z in range(step.z1, step.z2 + 1):
                    self.cuboids[x, y, z] = step.on


def solve(lines):
    steps = parse_steps(lines)
    reactor = Reactor(50, steps)
    reactor.reboot()
    return reactor.count_active_cubes()


if __name__ == '__main__':
    utils.solve(solve)

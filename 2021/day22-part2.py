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
        assert x1 < x2
        assert y1 < y2
        assert z1 < z2
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

    def contains(self, other):
        return (self.x1 <= other.x1 < other.x2 <= self.x2
                and self.y1 <= other.y1 < other.y2 <= self.y2
                and self.z1 <= other.z1 < other.z2 <= self.z2)

    def overlaps(self, other):
        def overlaps(min1, max1, min2, max2):
            return max1 >= min2 and max2 >= min1
        
        return (overlaps(self.x1, self.x2, other.x1, other.x2)
                and overlaps(self.y1, self.y2, other.y1, other.y2)
                and overlaps(self.z1, self.z2, other.z1, other.z2))

    def __str__(self):
        return f'{self.on} {self.x1}..{self.x2} {self.y1}..{self.y2} {self.z1}..{self.z2}'


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


def print_containment_stats(steps):
    """
    in the large example, nothing contains another
    in the input, 20 contain another
    total steps in the input: 420
    """
    for i1, s1 in enumerate(steps):
        for i2 in range(i1 + 1, len(steps)):
            s2 = steps[i2]
            if s1.contains(s2):
                print(f'{i1} contains {i2} ({s1}, {s2})')
            elif s2.contains(s1):
                print(f'{i2} contains {i1} ({s2}, {s1})')


def distinct_pairs(steps):
    for i1, s1 in enumerate(steps):
        for i2 in range(i1 + 1, len(steps)):
            yield i1, s1, i2, steps[i2]


def print_disjoint_stats(steps):
    """
    1 disjoint in example and 1 in input
    """
    for i1, s1 in enumerate(steps):
        for i2, s2 in enumerate(steps):
            if s1 == s2:
                continue

            if s1.overlaps(s2):
                break
        else:
            print(f'{i1} is disjoint ({s1})')


def print_overlap_stats(steps):
    """
    high number of overlaps, 5 to 15 are pretty common
    highest value seen in inut 23, in example 25
    """
    for i1, s1 in enumerate(steps):
        count = 0
        for i2, s2 in enumerate(steps):
            if s1 == s2:
                continue

            if s1.overlaps(s2):
                count += 1

        print(f'{i1} overlaps with count={count} ({s1})')


def print_connect_component_stats(g):
    """
    connected component sizes in input: 399, 20, 1
    connected component sizes in example: 50, 9, 1
    """
    roots = g.connected_components()
    print(Counter(roots))


def build_graph(steps):
    g = utils.Graph()
    for i1, s1, i2, s2 in distinct_pairs(steps):
        if s1.overlaps(s2):
            g.connect(i1, i2)

    for i1, _ in enumerate(steps):
        if i1 not in g.adj:
            g.connect(i1, i1)

    return g


def solve(lines):
    steps = list(parse_steps(lines))
    # range of ranges: -100k .. 100k
    # reactor = Reactor(50, steps)
    # print_containment_stats(steps)
    # print_disjoint_stats(steps)
    # print_overlap_stats(steps)
    g = build_graph(steps)
    print_connect_component_stats(g)

    # reactor.reboot()
    # return reactor.count_active_cubes()


if __name__ == '__main__':
    utils.solve(solve)

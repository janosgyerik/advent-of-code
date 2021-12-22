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
    def __init__(self, on, cuboid):
        self.on = on
        self.cuboid = cuboid


class Cuboid:
    def __init__(self, x1, x2, y1, y2, z1, z2):
        assert x1 <= x2
        assert y1 <= y2
        assert z1 <= z2
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.z1 = z1
        self.z2 = z2

    def volume(self):
        return (self.x2 - self.x1) * (self.y2 - self.y1) * (self.z2 - self.z1)

    def in_range(self, dim):
        return (-dim <= self.x1 <= self.x2 <= dim
                and -dim <= self.y1 <= self.y2 <= dim
                and -dim <= self.z1 <= self.z2 <= dim)

    def contains(self, other):
        return (self.x1 <= other.x1 <= other.x2 <= self.x2
                and self.y1 <= other.y1 <= other.y2 <= self.y2
                and self.z1 <= other.z1 <= other.z2 <= self.z2)

    def overlaps(self, other):
        def overlaps_1d(min1, max1, min2, max2):
            return max1 >= min2 and max2 >= min1

        return (overlaps_1d(self.x1, self.x2, other.x1, other.x2)
                and overlaps_1d(self.y1, self.y2, other.y1, other.y2)
                and overlaps_1d(self.z1, self.z2, other.z1, other.z2))

    def intersection(self, other):
        x = sorted([self.x1, self.x2, other.x1, other.x2])
        y = sorted([self.y1, self.y2, other.y1, other.y2])
        z = sorted([self.z1, self.z2, other.z1, other.z2])
        return Cuboid(x[1], x[2], y[1], y[2], z[1], z[2])

    def split_around(self, other):
        slices = []

        if other.contains(self):
            return slices

        assert self.overlaps(other)

        intersection = self.intersection(other)
        assert self.contains(intersection), f'expected {self} to contain {intersection}'

        shaved = self.copy()

        slices.append(shaved.left_of_x(intersection.x1))
        shaved = shaved.right_of_x(intersection.x1)
        slices.append(shaved.right_of_x(intersection.x2))
        shaved = shaved.left_of_x(intersection.x2)

        slices.append(shaved.left_of_y(intersection.y1))
        shaved = shaved.right_of_y(intersection.y1)
        slices.append(shaved.right_of_y(intersection.y2))
        shaved = shaved.left_of_y(intersection.y2)

        slices.append(shaved.left_of_z(intersection.z1))
        shaved = shaved.right_of_z(intersection.z1)
        slices.append(shaved.right_of_z(intersection.z2))
        shaved = shaved.left_of_z(intersection.z2)

        assert shaved.equals(intersection)

        # assert intersection.volume() + sum(c.volume() for c in slices) == self.volume()

        return [s for s in slices if not s.is_empty()]

    def copy(self):
        return Cuboid(self.x1, self.x2, self.y1, self.y2, self.z1, self.z2)

    def left_of_x(self, x):
        return Cuboid(self.x1, x, self.y1, self.y2, self.z1, self.z2)

    def right_of_x(self, x):
        return Cuboid(x, self.x2, self.y1, self.y2, self.z1, self.z2)

    def left_of_y(self, y):
        return Cuboid(self.x1, self.x2, self.y1, y, self.z1, self.z2)

    def right_of_y(self, y):
        return Cuboid(self.x1, self.x2, y, self.y2, self.z1, self.z2)

    def left_of_z(self, z):
        return Cuboid(self.x1, self.x2, self.y1, self.y2, self.z1, z)

    def right_of_z(self, z):
        return Cuboid(self.x1, self.x2, self.y1, self.y2, z, self.z2)

    def is_empty(self):
        return self.x1 == self.x2 or self.y1 == self.y2 or self.z1 == self.z2

    def equals(self, other):
        return (self.x1 == other.x1 and self.x2 == other.x2
                and self.y1 == other.y1 and self.y2 == other.y2
                and self.z1 == other.z1 and self.z2 == other.z2)

    def __str__(self):
        return f'{self.x1}..{self.x2} {self.y1}..{self.y2} {self.z1}..{self.z2}'

    def __repr__(self):
        return str(self)


class Cuboids:
    """ A collection of disjoint cuboids """

    def __init__(self):
        self.cuboids = []

    def volume(self):
        return sum(c.volume() for c in self.cuboids)

    def add(self, cuboid):
        self.remove(cuboid)
        self.cuboids.append(cuboid)

    def remove(self, cuboid):
        new_cuboids = []
        for c in self.cuboids:
            if not c.overlaps(cuboid):
                new_cuboids.append(c)
            else:
                new_cuboids.extend(c.split_around(cuboid))

        self.cuboids = new_cuboids


def parse_step(line):
    x1, x2, y1, y2, z1, z2 = utils.extract_all_valid_ints(line)
    return Step(line.startswith('on '), Cuboid(x1, x2 + 1, y1, y2 + 1, z1, z2 + 1))


def parse_steps(lines):
    for line in lines:
        yield parse_step(line)


class Reactor:
    def __init__(self, steps):
        self.steps = steps
        self.cuboids = Cuboids()

    def reboot(self):
        for step in self.steps:
            if step.on:
                self.cuboids.add(step.cuboid)
            else:
                self.cuboids.remove(step.cuboid)

    def count_active_cubes(self):
        return self.cuboids.volume()


def solve(lines):
    steps = list(parse_steps(lines))
    reactor = Reactor(steps)
    reactor.reboot()
    return reactor.count_active_cubes()


if __name__ == '__main__':
    utils.solve(solve)

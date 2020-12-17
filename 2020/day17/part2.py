#!/usr/bin/env python

import sys
from collections import namedtuple, Counter, deque, defaultdict
from itertools import product
from heapq import heappush, heappop, heapify
from functools import lru_cache


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


class Conway:
    def __init__(self, level0):
        d = len(level0)
        self.min_w = 0
        self.max_w = d - 1
        self.min_z = 0
        self.max_z = 0
        self.min_r = 0
        self.max_r = d - 1
        self.min_c = 0
        self.max_c = d - 1
        self.grid = {}
        for r, row in enumerate(level0):
            for c, x in enumerate(row):
                self.grid[0, 0, r, c] = x

    def simulate(self):
        copy = {}
        min_w = self.min_w
        max_w = self.max_w
        min_z = self.min_z
        max_z = self.max_z
        min_r = self.min_r
        max_r = self.max_r
        min_c = self.min_c
        max_c = self.max_c
        for w in range(self.min_w - 1, self.max_w + 2):
            for z in range(self.min_z - 1, self.max_z + 2):
                for r in range(self.min_r - 1, self.max_r + 2):
                    for c in range(self.min_c - 1, self.max_c + 2):
                        n = self.count_active_neighbors(w, z, r, c)
                        if self.is_active(w, z, r, c):
                            if n in {2, 3}:
                                self.update(copy, w, z, r, c, 1)
                                min_w = min(min_w, w)
                                max_w = max(max_w, w)
                                min_z = min(min_z, z)
                                max_z = max(max_z, z)
                                min_r = min(min_r, r)
                                max_r = max(max_r, r)
                                min_c = min(min_c, c)
                                max_c = max(max_c, c)
                            else:
                                self.update(copy, w, z, r, c, 0)
                        else:
                            if n == 3:
                                self.update(copy, w, z, r, c, 1)
                                min_w = min(min_w, w)
                                max_w = max(max_w, w)
                                min_z = min(min_z, z)
                                max_z = max(max_z, z)
                                min_r = min(min_r, r)
                                max_r = max(max_r, r)
                                min_c = min(min_c, c)
                                max_c = max(max_c, c)
                            else:
                                self.update(copy, w, z, r, c, 0)

        self.grid = copy
        self.min_w = min_w
        self.max_w = max_w
        self.min_z = min_z
        self.max_z = max_z
        self.min_r = min_r
        self.max_r = max_r
        self.min_c = min_c
        self.max_c = max_c

    def count_active_neighbors(self, w, z, r, c):
        neighs = set()
        for w2 in range(w - 1, w + 2):
            for z2 in range(z - 1, z + 2):
                for r2 in range(r - 1, r + 2):
                    for c2 in range(c - 1, c + 2):
                        neighs.add((w2, z2, r2, c2))

        neighs.remove((w, z, r, c))

        count = 0
        for w2, z2, r2, c2 in neighs:
            count += self.grid.get((w2, z2, r2, c2), 0)
        return count

    def is_active(self, w, z, r, c):
        return self.grid.get((w, z, r, c), 0) == 1

    def update(self, copy, w, z, r, c, v):
        copy[w, z, r, c] = v

    def count_active(self):
        count = 0
        for w in range(self.min_w, self.max_w + 1):
            for z in range(self.min_z, self.max_z + 1):
                for r in range(self.min_r, self.max_r + 1):
                    for c in range(self.min_c, self.max_c + 1):
                        count += self.grid.get((w, z, r, c), 0)

        return count


def conway_from_lines(lines):
    level0 = [[1 if x == '#' else 0 for x in line] for line in lines]
    return Conway(level0)


def main():
    lines = read_lines(sys.argv[1])
    m = conway_from_lines(lines)
    for _ in range(6):
        m.simulate()
    print(m.count_active())


if __name__ == '__main__':
    main()

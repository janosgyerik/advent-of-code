#!/usr/bin/env python

import sys
from collections import namedtuple

Loc = namedtuple('Loc', ['id', 'x', 'y'])


class Grid:
    def __init__(self, locs):
        self.locs = locs
        self.max_x = max(loc.x for loc in locs) + 1
        self.max_y = max(loc.y for loc in locs) + 1
        self.counts = dict((i, 0) for i in range(len(locs) + 1))

        self.grid = [[0 for _ in range(self.max_x)] for _ in range(self.max_y)]
        for loc in self.locs:
            self.grid[loc.y][loc.x] = loc.id

    def display(self):
        for row in self.grid:
            print(row)

    def safe_region_size(self, limit):
        size = 0
        for y in range(self.max_y):
            for x in range(self.max_x):
                if self.within_limit(x, y, limit):
                    size += 1
        return size

    def within_limit(self, x, y, limit):
        dist = 0
        for loc in locs:
            dist += self.dist(loc, x, y)
            if dist >= limit:
                return False

        return True

    def dist(self, loc, x, y):
        return abs(loc.x - x) + abs(loc.y - y)


locs = [Loc(i + 1, x, y) for i, (x, y) in
        enumerate((int(a), int(b)) for a, b in
            (s.rstrip().split(', ') for s in sys.stdin.readlines()))]

grid = Grid(locs)
limit = int(sys.argv[1])
print(grid.safe_region_size(limit))

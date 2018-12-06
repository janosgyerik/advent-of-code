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

    def fill_nearest(self):
        for y in range(self.max_y):
            for x in range(self.max_x):
                nearest_id = self.nearest_id(x, y)
                self.grid[y][x] = nearest_id
                self.counts[nearest_id] += 1

    def nearest_id(self, x, y):
        min_dist = self.max_x + self.max_y
        min_dist_id = 0
        for loc in locs:
            d = self.dist(loc, x, y)
            if d < min_dist:
                min_dist = d
                min_dist_id = loc.id
            elif d == min_dist:
                min_dist_id = 0
        return min_dist_id

    def dist(self, loc, x, y):
        return abs(loc.x - x) + abs(loc.y - y)

    def largest_area(self):
        copy = dict(self.counts)
        del copy[0]
        for x in self.grid[0]:
            if x in copy:
                del copy[x]
        for x in self.grid[-1]:
            if x in copy:
                del copy[x]
        for row in self.grid:
            if row[0] in copy:
                del copy[row[0]]
            if row[-1] in copy:
                del copy[row[-1]]
        return max(copy.values())


locs = [Loc(i + 1, x, y) for i, (x, y) in
        enumerate((int(a), int(b)) for a, b in
            (s.rstrip().split(', ') for s in sys.stdin.readlines()))]

grid = Grid(locs)
grid.fill_nearest()
print(grid.largest_area())

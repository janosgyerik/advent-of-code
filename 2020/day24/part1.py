#!/usr/bin/env python

import sys
from collections import defaultdict


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


def path_from_line(line):
    path = []
    index = 0
    while index < len(line):
        c = line[index]
        if c in 'ew':
            path.append(c)
            index += 1
        else:
            path.append(c + line[index + 1])
            index += 2

    return path


def paths_from_lines(lines):
    return [path_from_line(line) for line in lines]


dirs = {
    'e': (1, 0),
    'w': (-1, 0),
    'ne': (0, 1),
    'nw': (-1, 1),
    'se': (1, -1),
    'sw': (0, -1)
}


class Grid:
    def __init__(self):
        self.grid = defaultdict(int)

    def flip(self, path):
        x = y = 0
        for p in path:
            dx, dy = dirs[p]
            x += dx
            y += dy

        self.grid[x, y] = 1 - self.grid[x, y]

    def count_black(self):
        return sum(self.grid.values())

    def simulate(self):
        min_x = min_y = max_x = max_y = 0
        for x, y in self.grid.keys():
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)
        
        copy = self.grid.copy()
        for x in range(min_x - 1, max_x + 2):
            for y in range(min_y - 1, max_y + 2):
                neigh = self.count_black_neighbors(x, y)
                if self.grid[x, y] == 1:
                    if neigh == 0 or neigh > 2:
                        copy[x, y] = 0
                elif neigh == 2:
                    copy[x, y] = 1

        self.grid = copy

    def count_black_neighbors(self, x, y):
        count = 0
        for dx, dy in dirs.values():
            x2 = x + dx
            y2 = y + dy
            if self.grid[x2, y2] == 1:
                count += 1

        return count


def main():
    lines = read_lines(sys.argv[1])
    paths = paths_from_lines(lines)
    grid = Grid()
    for path in paths:
        grid.flip(path)
    print(grid.count_black())

    for _ in range(100):
        grid.simulate()

    print(grid.count_black())


if __name__ == '__main__':
    main()

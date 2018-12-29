#!/usr/bin/env python

import sys


class Landscape:
    OPEN = '.'
    TREES = '|'
    LUMBERS = '#'
    DXY = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))

    def __init__(self, grid):
        self.grid = grid
        self.mx = len(grid[0])
        self.my = len(grid)

    def display(self):
        print(*(''.join(row) for row in self.grid), sep='\n')

    def has_adjacent(self, x, y, content, mincount):
        count = 0
        for dx, dy in self.DXY:
            x2 = x + dx
            y2 = y + dy
            if self.is_valid(x2, y2) and self.grid[y2][x2] == content:
                count += 1
                if count == mincount:
                    return True

        return False

    def is_valid(self, x, y):
        return 0 <= x < self.mx and 0 <= y < self.my

    def transform(self):
        g2 = [['.'] * self.mx for _ in range(self.my)]
        for y in range(self.my):
            for x in range(self.mx):
                before = self.grid[y][x]
                if before == self.OPEN:
                    after = self.TREES if self.has_adjacent(x, y, self.TREES, 3) else before

                elif before == self.TREES:
                    after = self.LUMBERS if self.has_adjacent(x, y, self.LUMBERS, 3) else before

                elif before == self.LUMBERS:
                    after = self.LUMBERS if self.has_adjacent(x, y, self.TREES, 1) and self.has_adjacent(x, y, self.LUMBERS, 1) else self.OPEN

                else:
                    raise RuntimeError('Illegal tile content: ' + current)

                g2[y][x] = after

        self.grid = g2

    def transform_n(self, n):
        for _ in range(n):
            self.transform()

    def value(self):
        trees = sum(row.count(self.TREES) for row in self.grid)
        lumbers = sum(row.count(self.LUMBERS) for row in self.grid)
        return trees * lumbers


def parse_grid(lines):
    return [[x for x in line.rstrip()] for line in lines]

if __name__ == '__main__':
    grid = parse_grid(sys.stdin.readlines())
    landscape = Landscape(grid)
    landscape.transform_n(10)
    landscape.display()
    print(landscape.value())

#!/usr/bin/env python

import sys


class Sim:
    def __init__(self, grid):
        self.grid = grid

    def _copy_grid(self, grid):
        return [[x for x in row] for row in grid]

    def _print_grid(self, grid):
        for row in grid:
            print(''.join(row))
        print()

    def _count_occupied(self, grid):
        count = 0
        
        for r, row in enumerate(grid):
            for c, x in enumerate(row):
                if x == '#':
                    count += 1

        return count

    def simulate(self):
        i = 0
        while True:
            changes = self.simulate_once()
            if i < 3:
                i += 1
                self._print_grid(self.grid)
            if changes == 0:
                return self._count_occupied(self.grid)

    def simulate_once(self):
        copy = self._copy_grid(self.grid)

        changes = 0

        for r, row in enumerate(self.grid):
            for c, x in enumerate(row):
                if x == '.':
                    continue

                occupied_neighbors = self.count_occupied_neighbors(self.grid, r, c)
                if x == 'L':
                    if occupied_neighbors == 0:
                        copy[r][c] = '#'
                        changes += 1

                else:
                    if occupied_neighbors >= 4:
                        copy[r][c] = 'L'
                        changes += 1

        self.grid = copy

        return changes

    def count_occupied_neighbors(self, grid, r, c):
        rows = len(grid)
        cols = len(grid[0])

        count = 0
        for r2, c2 in (r+1, c), (r-1, c), (r, c+1), (r, c-1), (r+1, c+1), (r-1, c-1), (r+1, c-1), (r-1, c+1):
            if 0 <= r2 < rows and 0 <= c2 < cols and grid[r2][c2] == '#':
                count += 1

        return count


def grid_from_lines(lines):
    return [[x for x in line] for line in lines]


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


def main():
    lines = read_lines(sys.argv[1])
    grid = grid_from_lines(lines)
    sim = Sim(grid)
    occupied = sim.simulate()
    print(occupied)


if __name__ == '__main__':
    main()

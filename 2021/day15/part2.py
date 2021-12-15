#!/usr/bin/env python
import re
import sys
from collections import namedtuple, Counter, deque, defaultdict
from itertools import product
from heapq import heappush, heappop, heapify
from functools import lru_cache
from typing import List

import utils


class Foo:
    def __init__(self):
        pass

    def print(self):
        print('todo: print')


class Grid:
    def __init__(self, grid):
        self.grid = grid
        self.size = len(grid)

    def print(self):
        for row in self.grid:
            print(''.join(str(x) for x in row))

    def new_value(self, value, offset):
        value += offset
        if value >= 10:
            value -= 9
        return value

    def add_to_right(self, offset):
        for index in range(self.size):
            row = self.grid[index][:self.size]
            self.grid[index].extend(row)

            for index2 in range(self.size):
                base = len(self.grid[index]) - self.size
                value = self.new_value(row[index2], offset)
                self.grid[index][base + index2] = value

    def add_to_bottom(self, offset):
        base_row_index = len(self.grid)

        for index in range(self.size):
            row = self.grid[index]
            self.grid.append(row[:])

            for index2, value in enumerate(row):
                self.grid[base_row_index + index][index2] = self.new_value(value, offset)

    def multiply(self):
        for offset in range(4):
            self.add_to_right(offset + 1)

        for offset in range(4):
            self.add_to_bottom(offset + 1)


def create_graph(grid):
    size = len(grid)
    g = utils.Graph()
    for r, row in enumerate(grid):
        for c, _ in enumerate(row):
            for r2, c2 in (r + 1, c), (r, c + 1):
                if r2 < size and c2 < size:
                    g.connect((r, c), (r2, c2))

    return g


def solve(lines):
    grid = Grid(utils.strings_of_digits_to_grid_of_ints(lines))
    grid.multiply()

    def weight_getter(source, target):
        r, c = target
        return grid.grid[r][c]

    graph = create_graph(grid.grid)
    last = len(grid.grid) - 1

    return utils.dijkstra(graph, (0, 0), (last, last), weight_getter=weight_getter)


def main():
    lines = utils.read_lines(sys.argv[1])
    print(solve(lines))


if __name__ == '__main__':
    main()

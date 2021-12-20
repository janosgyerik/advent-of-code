#!/usr/bin/env python
import math

import utils
import re
from collections import namedtuple, Counter, deque, defaultdict
from itertools import product
from heapq import heappush, heappop, heapify
from functools import lru_cache
import utils


def line_to_digits(line):
    return [1 if c == '#' else 0 for c in line]


def parse_mapping(line):
    return dict(enumerate(line_to_digits(line)))


def parse_image(mapping, lines):
    grid = [line_to_digits(line) for line in lines]
    return Image(grid, mapping)


class Image:
    def __init__(self, grid, mapping):
        self.grid = grid
        self.mapping = mapping
        self.padding = 0
        self.flip_padding = mapping[0] == 1

    def print(self):
        for row in self.grid:
            print(''.join('.' if x == 0 else '#' for x in row))

        print()

    def enhance(self):
        self.add_padding()
        self._enhance()

        if self.flip_padding:
            self.padding = 1 - self.padding

        self.shave_padding()

    def add_padding(self):
        cols = len(self.grid[0])

        width = 3
        edge_padding = [self.padding] * width
        full_padding = [self.padding] * cols + (2 * edge_padding)

        new_grid = []
        for _ in range(width):
            new_grid.append(full_padding)

        for row in self.grid:
            new_grid.append(edge_padding + row + edge_padding)

        for _ in range(width):
            new_grid.append(full_padding)

        self.grid = new_grid

    def count_pixels(self):
        return sum(sum(row) for row in self.grid)

    def _enhance(self):
        grid = []
        for r in range(1, len(self.grid) - 1):
            row = []
            grid.append(row)
            for c in range(1, len(self.grid[0]) - 1):
                row.append(self.compute_new_cell(r, c))

        self.grid = grid

    def shave_padding(self):
        start = self.skip_full_padding(0, 1)
        end = self.skip_full_padding(len(self.grid) - 1, -1)
        self.grid = self.grid[start:end+1]

        left = self.skip_edge_padding(0, 1)
        right = self.skip_edge_padding(len(self.grid[0]) - 1, -1)

        self.grid = [row[left:right+1] for row in self.grid]

    def skip_full_padding(self, index, step):
        while True:
            if not self.is_full_padding(index):
                return index

            index += step

    def skip_edge_padding(self, index, step):
        while True:
            if not self.is_vertical_padding(index):
                return index

            index += step

    def is_full_padding(self, index):
        return all(c == self.padding for c in self.grid[index])

    def is_vertical_padding(self, index):
        return all(row[index] == self.padding for row in self.grid)

    def compute_new_cell(self, r, c):
        key = self.triplet_to_int(r - 1, c - 1)
        key <<= 3
        key += self.triplet_to_int(r, c - 1)
        key <<= 3
        key += self.triplet_to_int(r + 1, c - 1)
        return self.mapping[key]

    def triplet_to_int(self, r, c):
        value = self.grid[r][c]
        value <<= 1
        value += self.grid[r][c+1]
        value <<= 1
        value += self.grid[r][c+2]
        return value


def solve(lines):
    mapping = parse_mapping(lines[0])
    image = parse_image(mapping, lines[2:])
    for _ in range(50):
        image.enhance()
    # image.print()
    return image.count_pixels()


if __name__ == '__main__':
    utils.solve(solve)

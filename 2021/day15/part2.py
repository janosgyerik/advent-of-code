#!/usr/bin/env python
import re
import sys
from collections import namedtuple, Counter, deque, defaultdict
from itertools import product
from heapq import heappush, heappop, heapify
from functools import lru_cache
from typing import List

import utils


def new_value(value, offset):
    value += offset
    if value >= 10:
        value -= 9
    return value


def reshape(base):
    dim = len(base)
    new_dim = dim * 5

    grid = [[0] * new_dim for _ in range(new_dim)]

    for r in range(new_dim):
        for c in range(new_dim):
            r0 = r % dim
            c0 = c % dim
            offset = r // dim + c // dim
            grid[r][c] = new_value(base[r0][c0], offset)

    return grid


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
    grid = utils.strings_of_digits_to_grid_of_ints(lines)
    grid = reshape(grid)

    def weight_getter(source, target):
        r, c = target
        return grid[r][c]

    graph = create_graph(grid)
    last = len(grid) - 1

    return utils.dijkstra(graph, (0, 0), (last, last), weight_getter=weight_getter)


def main():
    lines = utils.read_lines(sys.argv[1])
    print(solve(lines))


if __name__ == '__main__':
    main()

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


def min_path_sum(grid: List[List[int]]) -> int:
    rows = len(grid)
    cols = len(grid[0])

    memo = {}

    def helper(r, c):
        if (r, c) in memo:
            return memo[(r, c)]

        m = grid[r][c]
        if r + 1 == rows and c + 1 == cols:
            return m

        if r + 1 < rows and c + 1 < cols:
            m += min(helper(r + 1, c), helper(r, c + 1))
        elif r + 1 < rows:
            m += helper(r + 1, c)
        else:
            m += helper(r, c + 1)

        memo[(r, c)] = m
        return m

    return helper(0, 0)


def solve(lines):
    grid = utils.strings_of_digits_to_grid_of_ints(lines)
    return min_path_sum(grid) - grid[0][0]


def main():
    lines = utils.read_lines(sys.argv[1])
    print(solve(lines))


if __name__ == '__main__':
    main()

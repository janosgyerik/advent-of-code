#!/usr/bin/env python

import sys
from collections import namedtuple, Counter, deque, defaultdict
from dataclasses import dataclass
from functools import lru_cache
from heapq import heappush, heappop, heapify
from itertools import product


def ints(line):
    return [int(x) for x in line.split(' ')]


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


def solve(lines):
    dim = len(lines)
    grid = [[int(x) for x in line] for line in lines]

    counted = set()
    count = 0
    for r in range(dim):
        highest = -1
        last = 0
        for c in range(dim):
            x = grid[r][c]
            if x > highest:
                if (r, c) not in counted:
                    count += 1
                    counted.add((r, c))
                highest = x
                last = c

        highest = -1
        for c in range(dim - 1, -1, -1):
            if c == last:
                break

            x = grid[r][c]
            if x > highest:
                if (r, c) not in counted:
                    count += 1
                    counted.add((r, c))
                highest = x

    for c in range(dim):
        highest = -1
        last = 0
        for r in range(dim):
            x = grid[r][c]
            if x > highest:
                if (r, c) not in counted:
                    count += 1
                    counted.add((r, c))
                highest = x
                last = r

        highest = -1
        for r in range(dim - 1, -1, -1):
            if r == last:
                break

            x = grid[r][c]
            if x > highest:
                if (r, c) not in counted:
                    count += 1
                    counted.add((r, c))
                highest = x

    return count


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines))


if __name__ == '__main__':
    main()

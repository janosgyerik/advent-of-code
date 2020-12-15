#!/usr/bin/env python

import sys
from collections import namedtuple, Counter, deque, defaultdict
from itertools import product
from heapq import heappush, heappop, heapify
from functools import lru_cache


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


def part1(nums, n):
    first = {}
    for index, x in enumerate(nums):
        first[x] = index

    second = {}

    last = nums[-1]
    for index in range(len(nums), n):
        if last not in second:
            current = 0
        else:
            current = second[last] - first[last]

        if current not in first:
            first[current] = index
        elif current not in second:
            second[current] = index
        else:
            first[current] = second[current]
            second[current] = index

        last = current

    return last


def main():
    lines = read_lines(sys.argv[1])
    nums = [int(x) for x in lines[0].split(',')]
    print(part1(nums, 2020))
    print(part1(nums, 30000000))


if __name__ == '__main__':
    main()

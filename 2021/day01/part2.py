#!/usr/bin/env python

import sys
from collections import namedtuple, Counter, deque, defaultdict
from itertools import product
from heapq import heappush, heappop, heapify
from functools import lru_cache


def ints(line):
    return [int(x) for x in line.split(' ')]


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


def solve(lines):
    count = 0
    nums = [int(v) for v in lines]
    wlen = 3
    window = sum(nums[0:wlen])
    index = wlen
    n = len(nums)
    prev = window
    while index < n:
        window += nums[index] - nums[index - wlen]
        if prev < window:
            count += 1
        prev = window
        index += 1

    return count


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines))


if __name__ == '__main__':
    main()

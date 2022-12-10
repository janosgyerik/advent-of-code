#!/usr/bin/env python
import functools
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


def x_at(seq, c):
    prev = 0
    for cycle, x in seq:
        if cycle == c:
            return x
        if c < cycle:
            return prev
        prev = x

    raise ValueError("not found")


def solve(lines):
    cycles = 1
    x = 1
    seq = [(1, 0)]

    for line in lines:
        if line == 'noop':
            cycles += 1
        elif line.startswith('addx '):
            x += int(line.split()[1])
            cycles += 2
        else:
            raise ValueError(f"unexpected line: {line}")

        seq.append((cycles, x))

    return sum(c * x_at(seq, c) for c in [20, 60, 100, 140, 180, 220])


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines))


if __name__ == '__main__':
    main()

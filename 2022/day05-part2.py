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


class Crates:
    def __init__(self, n):
        self.crates = [[] for _ in range(n)]

    def add(self, pos, c):
        self.crates[pos].append(c)

    def print(self):
        for crate in self.crates:
            print(crate)

    def move(self, count, source, target):
        self.crates[target].extend(self.crates[source][-count:])
        self.crates[source][-count:] = []

    def tips(self):
        return ''.join([c[-1] for c in self.crates])


def solve(lines):
    n = 9
    crates = Crates(n)
    index = 0
    for line in lines:
        if line.startswith(' '):
            break
        index += 1

    index0 = index + 2
    for index in range(index - 1, -1, -1):
        line = lines[index]
        for pos in range(n + 1):
            c = pos * 4 + 1
            if c > len(line):
                continue

            if line[c] != ' ':
                crates.add(pos, line[c])

    crates.print()

    for line in lines[index0:]:
        parts = line.split()
        count, source, target = [int(x) for x in (parts[1], parts[3], parts[5])]
        crates.move(count, source - 1, target - 1)

    crates.print()
    return crates.tips()


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines))


if __name__ == '__main__':
    main()

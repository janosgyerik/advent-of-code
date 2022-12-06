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
    lastpos = {}
    candidates = set()
    length = 4

    datastream = lines[0]
    for pos, c in enumerate(datastream):
        if pos >= length:
            oldc = datastream[pos - length]
            if lastpos[oldc] == pos - length:
                candidates.remove(oldc)

        candidates.add(c)
        lastpos[c] = pos

        if len(candidates) == length:
            return pos + 1


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines))


if __name__ == '__main__':
    main()

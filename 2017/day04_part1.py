#!/usr/bin/env python

import codebook
import re
from collections import namedtuple, Counter, deque, defaultdict
from itertools import product
from heapq import heappush, heappop, heapify
from functools import lru_cache


def is_valid(line):
    words = line.split()
    return len(words) == len(set(words))


def solve(lines):
    total = 0
    for line in lines:
        if is_valid(line):
            total += 1

    return total


if __name__ == '__main__':
    codebook.solve(solve)

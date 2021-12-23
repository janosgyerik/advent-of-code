#!/usr/bin/env python

import codebook
import re
from collections import namedtuple, Counter, deque, defaultdict
from itertools import product
from heapq import heappush, heappop, heapify
from functools import lru_cache


def normalized(word):
    return ''.join(sorted(word))


def normalized_list(words):
    return [normalized(word) for word in words]


def is_valid(line):
    words = line.split()
    return len(words) == len(set(normalized_list(words)))


def solve(lines):
    total = 0
    for line in lines:
        if is_valid(line):
            total += 1

    return total


if __name__ == '__main__':
    codebook.solve(solve)

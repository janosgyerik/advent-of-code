#!/usr/bin/env python
import math

import utils
import re
from collections import namedtuple, Counter, deque, defaultdict
from itertools import product
from heapq import heappush, heappop, heapify
from functools import lru_cache


def parse_nodes(lines):
    arrow = ' -> '
    for line in lines:
        if arrow in line:
            left, right = line.split(arrow)
            yield left.split()[0], right.split(', ')
        else:
            yield line.split()[0], []


def solve(lines):
    dependents = set()
    names = set()
    for name, children in parse_nodes(lines):
        names.add(name)
        for child in children:
            dependents.add(child)

    for name in names:
        if name not in dependents:
            return name


if __name__ == '__main__':
    utils.solve(solve)

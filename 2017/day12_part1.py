#!/usr/bin/env python
import math

import utils
import re
from collections import namedtuple, Counter, deque, defaultdict
from itertools import product
from heapq import heappush, heappop, heapify
from functools import lru_cache
from dataclasses import dataclass
from utils import UnionFind


def solve(lines):
    uf = UnionFind(2000)
    for line in lines:
        p0, others = line.split(' <-> ')
        others = others.split(', ')

        p0 = int(p0)
        others = [int(x) for x in others]
        for v in others:
            uf.union(p0, v)

    count = 0
    for u in range(2000):
        if uf.find(0) == uf.find(u):
            count += 1

    return count


if __name__ == '__main__':
    utils.solve(solve)

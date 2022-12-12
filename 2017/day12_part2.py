#!/usr/bin/env python
import math

import utils
import re
from collections import namedtuple, Counter, deque, defaultdict
from itertools import product
from heapq import heappush, heappop, heapify
from functools import lru_cache
from dataclasses import dataclass


def solve(lines):
    uf = utils.UnionFindAutoMapper()
    for line in lines:
        p0, others = line.split(' <-> ')
        others = others.split(', ')

        for v in others:
            uf.union(p0, v)

    seen = set()
    for u in uf.keys():
        seen.add(uf.find(u))

    return len(seen)


if __name__ == '__main__':
    utils.solve(solve)

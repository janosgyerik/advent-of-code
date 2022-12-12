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
    fw = []
    for line in lines:
        depth, range_ = utils.extract_all_valid_ints(line)
        fw.append((depth, range_))

    severity = 0
    for d, r in fw:
        p = (r - 1) * 2
        if d % p == 0:
            severity += d * r

    return severity


if __name__ == '__main__':
    utils.solve(solve)

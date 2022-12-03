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
    total = 0
    level = 0
    in_garbage = False
    escape_next = False

    for c in lines[0]:
        if escape_next:
            escape_next = False
            continue

        if in_garbage:
            if c == '>':
                in_garbage = False
            elif c == '!':
                escape_next = True

            continue

        if c == '{':
            level += 1
        elif c == '}':
            total += level
            level -= 1
        elif c == '<':
            in_garbage = True

    return total


if __name__ == '__main__':
    utils.solve(solve)

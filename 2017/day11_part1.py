#!/usr/bin/env python
import math

import utils
import re
from collections import namedtuple, Counter, deque, defaultdict
from itertools import product
from heapq import heappush, heappop, heapify
from functools import lru_cache
from dataclasses import dataclass

DIRS = {
    'n': lambda a, r, c: (1 - a, r - (1 - a), c + a),
    'ne': lambda a, r, c: (a, r, c + 1),
    'se': lambda a, r, c: (1 - a, r + a, c + a),
    's': lambda a, r, c: (1 - a, r + a, c - (1 - a)),
    'sw': lambda a, r, c: (a, r, c - 1),
    'nw': lambda a, r, c: (1 - a, r - (1 - a), c - (1 - a)),
}


class HexGrid:
    def __init__(self):
        self.pos = 0, 0, 0

    def move(self, d):
        self.pos = DIRS[d](*self.pos)

    def dist_from(self, pos):
        q = deque([pos])
        seen = {pos}
        dist = 0
        while q:
            for _ in range(len(q)):
                current = q.popleft()
                if current == self.pos:
                    return dist

                for df in DIRS.values():
                    pos2 = df(*current)
                    if pos2 not in seen:
                        seen.add(pos2)
                        q.append(pos2)

            dist += 1


def solve(lines):
    hg = HexGrid()
    for d in lines[0].split(','):
        hg.move(d)

    print(hg.pos)
    return hg.dist_from((0, 0, 0))


if __name__ == '__main__':
    utils.solve(solve)

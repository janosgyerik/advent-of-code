#!/usr/bin/env python

import codebook
import re
from collections import namedtuple, Counter, deque, defaultdict
from itertools import product
from heapq import heappush, heappop, heapify
from functools import lru_cache


class Machine:
    def __init__(self, instructions):
        self.instructions = instructions
        self.index = 0

    def execute(self):
        oldindex = self.index
        self.index += self.instructions[self.index]
        self.instructions[oldindex] += 1

    def is_end(self):
        return self.index >= len(self.instructions)


def solve(lines):
    m = Machine(codebook.lines_to_ints(lines))

    count = 0
    while not m.is_end():
        m.execute()
        count += 1

    return count


if __name__ == '__main__':
    codebook.solve(solve)

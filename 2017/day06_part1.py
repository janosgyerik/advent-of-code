#!/usr/bin/env python
import math

import codebook
import re
from collections import namedtuple, Counter, deque, defaultdict
from itertools import product
from heapq import heappush, heappop, heapify
from functools import lru_cache


def find_max_index(nums):
    return max(range(len(nums)), key=lambda index: nums[index])


class Machine:
    def __init__(self, banks):
        self.banks = banks
        self.n = len(banks)
        self.seen = set(tuple(banks))

    def redistribute(self):
        max_index = find_max_index(self.banks)
        max_value = self.banks[max_index]

        share = math.ceil(max_value / self.n)
        self.banks[max_index] = 0

        for offset in range(1, self.n + 1):
            index = (max_index + offset) % self.n
            self.banks[index] += min(share, max_value)
            max_value -= share
            if max_value <= 0:
                break

        t = tuple(self.banks)
        if t in self.seen:
            return False

        self.seen.add(t)
        return True


def solve(lines):
    m = Machine(codebook.parse_ints(lines[0]))

    count = 1
    while m.redistribute():
        count += 1

    return count


if __name__ == '__main__':
    codebook.solve(solve)

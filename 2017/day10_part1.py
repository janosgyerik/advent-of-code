#!/usr/bin/env python
import math

import utils
import re
from collections import namedtuple, Counter, deque, defaultdict
from itertools import product
from heapq import heappush, heappop, heapify
from functools import lru_cache
from dataclasses import dataclass


class Hasher:
    def __init__(self, size):
        self.size = size
        self.nums = [x for x in range(size)]
        self.pos = 0
        self.skip = 0

    def apply(self, length):
        self._reverse_range(self.pos, length)
        self.pos = self._normalize_index(self.pos + length + self.skip)
        self.skip += 1

    def _reverse_range(self, start, length):
        left = start
        right = self._normalize_index(start + length - 1)
        for _ in range(length // 2):
            self.nums[left], self.nums[right] = self.nums[right], self.nums[left]
            left = self._normalize_index(left + 1)
            right = self._normalize_index(right - 1)

    def _normalize_index(self, index):
        if index < 0:
            return index + self.size

        return index % self.size

    def checksum(self):
        return self.nums[0] * self.nums[1]


def solve(lines):
    lengths = utils.extract_all_valid_ints(lines[0])
    size = 256
    # lengths = [3, 4, 1, 5]
    # size = 5
    h = Hasher(size)
    for length in lengths:
        h.apply(length)
        print(h.nums)

    return h.checksum()


if __name__ == '__main__':
    utils.solve(solve)

#!/usr/bin/env python
import re
import sys
from collections import namedtuple, Counter, deque, defaultdict
from itertools import product
from heapq import heappush, heappop, heapify
from functools import lru_cache

import utils


class Polymer:
    def __init__(self, polymer, mappings):
        self.polymer = polymer
        self.mappings = mappings

    def step(self):
        new_polymer = []
        for i in range(len(self.polymer) - 1):
            new_polymer.append(self.polymer[i])
            new_polymer.append(self.mappings[self.polymer[i:i+2]])

        new_polymer.append(self.polymer[-1])

        self.polymer = ''.join(new_polymer)

    def print(self):
        print(self.polymer)

    def answer(self):
        counts = Counter(self.polymer)
        most_common = max(counts.values())
        least_common = min(counts.values())
        return most_common - least_common


def parse_input(lines):
    s = lines[0]

    rules = {}
    for line in lines[2:]:
        pattern, mapping = line.split(' -> ')
        rules[pattern] = mapping

    return Polymer(s, rules)


def solve(lines):
    polymer = parse_input(lines)

    for _ in range(10):
        polymer.step()

    return polymer.answer()


def main():
    lines = utils.read_lines(sys.argv[1])
    print(solve(lines))


if __name__ == '__main__':
    main()

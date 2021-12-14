#!/usr/bin/env python
import math
import re
import sys
from collections import namedtuple, Counter, deque, defaultdict
from itertools import product
from heapq import heappush, heappop, heapify
from functools import lru_cache

import utils


class Polymer:
    def __init__(self, polymer, mappings):
        self.orig_polymer = polymer
        self.polymer = defaultdict(int)
        for i in range(len(polymer) - 1):
            self.polymer[polymer[i:i+2]] += 1
        self.mappings = mappings

    def step(self):
        new_polymer = defaultdict(int)
        for polymer, count in self.polymer.items():
            left = polymer[0] + self.mappings[polymer]
            right = self.mappings[polymer] + polymer[1]
            new_polymer[left] += count
            new_polymer[right] += count

        self.polymer = new_polymer

    def print(self):
        print(self.polymer)

    def answer(self):
        counts = Counter()
        for p, count in self.polymer.items():
            counts[p[0]] += count
            counts[p[1]] += count

        # the first and last letters of the template
        # were only counted once
        counts[self.orig_polymer[0]] += 1
        counts[self.orig_polymer[-1]] += 1

        # all the counts are doubled; for example for ABCD
        # B was counted twice for AB and BC
        # C was counted twice for BC and CD
        # A and D were counted twice in the extra treatment
        most_common = max(counts.values()) // 2
        least_common = min(counts.values()) // 2
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

    for _ in range(40):
        polymer.step()

    return polymer.answer()


def main():
    lines = utils.read_lines(sys.argv[1])
    print(solve(lines))


if __name__ == '__main__':
    main()

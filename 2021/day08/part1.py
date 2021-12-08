#!/usr/bin/env python
import re
import sys
from collections import namedtuple, Counter, deque, defaultdict
from itertools import product
from heapq import heappush, heappop, heapify
from functools import lru_cache


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


def lines_to_ints(lines):
    return [int(x) for x in lines[0].split(',')]


possibles_by_length = {
    2: (1, ),
    3: (7, ),
    4: (4, ),
    5: (2, 3, 5),
    6: (0, 6, 9),
    7: (8, ),
}


class Entry:
    def __init__(self, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs

    def count_outputs_of_lengths(self, targets):
        return sum(1 for x in self.outputs if len(x) in targets)


def parse_entries(lines):
    for line in lines:
        inputs, outputs = line.split(' | ')
        inputs = inputs.split()
        outputs = outputs.split()
        yield Entry(inputs, outputs)


def solve(lines):
    entries = parse_entries(lines)
    count = 0
    for entry in entries:
        count += entry.count_outputs_of_lengths({2, 3, 4, 7})

    return count


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines))


if __name__ == '__main__':
    main()

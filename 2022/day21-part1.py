#!/usr/bin/env python
import functools
import re
import sys
from collections import namedtuple, Counter, deque, defaultdict
from dataclasses import dataclass, field
from functools import lru_cache
from heapq import heappush, heappop, heapify
from itertools import product
from typing import Callable, List, Set, Tuple, Dict

from utils.binary_search import binary_search
from utils import parsing
from utils import coordinates
from enum import Enum, auto


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


def parse_nums(lines):
    for line in lines:
        yield int(line)


OPS = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a // b,
}


def parse_monkeys(lines):
    monkeys = {}
    for line in lines:
        name = line[:4]
        parts = line.split()
        if len(parts) == 2:
            monkeys[name] = int(parts[1]), None, None
        else:
            _, left, op, right = parts
            assert op in '+-*/'
            assert not isinstance(left, int)
            assert not isinstance(right, int)

            monkeys[name] = OPS[op], left, right

    return monkeys


def compute(monkeys, target):
    @lru_cache(maxsize=None)
    def compute2(name):
        if monkeys[name][1] is None:
            return monkeys[name][0]

        op, left, right = monkeys[name]
        return op(compute2(left), compute2(right))

    return compute2(target)


def solve(lines, *args):
    monkeys = parse_monkeys(lines)
    return compute(monkeys, 'root')


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines, *(sys.argv[2:])))


if __name__ == '__main__':
    main()

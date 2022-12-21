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


def add(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return a + b

    if isinstance(a, tuple):
        x, m, c = a
        return x, m, c + b

    if isinstance(b, tuple):
        x, m, c = b
        return x, m, c + a


def sub(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return a - b

    if isinstance(a, tuple):
        x, m, c = a
        return x, m, c - b

    if isinstance(b, tuple):
        x, m, c = b
        return x, -m, a - c

    return '-', a, b


def mul(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return a * b

    if isinstance(a, tuple):
        x, m, c = a
        return x, m * b, c * b

    if isinstance(b, tuple):
        x, m, c = b
        return x, m * a, c * a

    return '*', a, b


def div(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return a // b

    if isinstance(a, tuple):
        x, m, c = a
        return x, m / b, c / b

    if isinstance(b, tuple):
        x, m, c = b
        return x, a / m, a / c

    return '/', a, b


OPS = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': div,
}


def parse_monkeys(lines):
    monkeys = {}
    for line in lines:
        name = line[:4]
        parts = line.split()
        if len(parts) == 2:
            monkeys[name] = [int(parts[1]), None, None]
        else:
            _, left, op, right = parts
            assert op in OPS
            assert not isinstance(left, int)
            assert not isinstance(right, int)

            monkeys[name] = OPS[op], left, right

    return Monkeys(monkeys)


@dataclass
class Monkeys:
    monkeys: Dict[str, any]

    def compute_root(self):
        left, right = self.monkeys['root'][1:]
        self.monkeys['humn'] = 'x', 1, 0
        left = self.compute(left)
        right = self.compute(right)
        print('left =', left)
        print('right =', right)

        x, m, c = left
        z = (right - c) / m
        return z, int(z)

    def compute(self, name):
        v = self.monkeys[name]
        op, left, right = v
        if op == 'x':
            return v

        if left is None:
            return op

        return op(self.compute(left), self.compute(right))


def solve(lines, *args):
    monkeys = parse_monkeys(lines)
    return monkeys.compute_root()


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines, *(sys.argv[2:])))


if __name__ == '__main__':
    main()

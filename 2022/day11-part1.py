#!/usr/bin/env python
from utils import parsing
import functools
import re
import sys
from collections import namedtuple, Counter, deque, defaultdict
from dataclasses import dataclass
from functools import lru_cache
from heapq import heappush, heappop, heapify
from itertools import product
from typing import Callable, List

from utils.binary_search import binary_search

re_natnums = re.compile(r'(?P<int>\d+)')


def ints(s):
    return [int(x) for x in s.split()]


def natnums(s):
    """
    >>> natnums("foo divisible by 3 and 2")
    [3, 2]
    """
    return [int(x) for x in re_natnums.findall(s)]


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


@dataclass
class Monkey:
    items: list
    op: Callable
    div: int
    true_target: int
    false_target: int


class Monkeys:
    def __init__(self, monkeys):
        self.monkeys = monkeys
        self.counts = [0] * len(monkeys)

    def play(self):
        for i, m in enumerate(self.monkeys):
            for item in m.items:
                self.counts[i] += 1
                item = m.op(item)
                item //= 3
                if item % m.div == 0:
                    new_target = m.true_target
                else:
                    new_target = m.false_target

                self.monkeys[new_target].items.append(item)

            m.items.clear()

    def print(self):
        for i, m in enumerate(self.monkeys):
            print(f"Monkey {i}, {self.counts[i]}:", ', '.join(str(x) for x in m.items))


def parse_monkeys(lines):
    def mul(t):
        return lambda x: x * t

    def square():
        return lambda x: x * x

    def plus(t):
        return lambda x: x + t

    def double():
        return lambda x: x + x

    re_template = r'''
Monkey \d:
  Starting items: (?P<natnums>.+)
  Operation: new = (?P<raw_op>.+)
  Test: divisible by (?P<div>\d+)
    If true: throw to monkey (?P<true_target>\d)
    If false: throw to monkey (?P<false_target>\d)
    '''.strip()
    monkeys = []
    for match in parsing.items_from_template_from_lines(re_template, lines):
        items = natnums(match.group('natnums'))
        op_line = match.group('raw_op')
        if 'old * old' in op_line:
            op = square()
        elif 'old + old' in op_line:
            op = double()
        else:
            op_arg = natnums(op_line)[0]
            if '*' in op_line:
                op = mul(op_arg)
            else:
                op = plus(op_arg)

        div = int(match.group('div'))
        true_target = int(match.group('true_target'))
        false_target = int(match.group('false_target'))

        monkeys.append(Monkey(items, op, div, true_target, false_target))

    return Monkeys(monkeys)


def solve(lines):
    m = parse_monkeys(lines)
    for _ in range(20):
        m.play()
    m.print()

    a, b = sorted(m.counts)[-2:]
    return a * b


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines))


if __name__ == '__main__':
    main()

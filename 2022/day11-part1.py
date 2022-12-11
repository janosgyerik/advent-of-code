#!/usr/bin/env python
import functools
import sys
from collections import namedtuple, Counter, deque, defaultdict
from dataclasses import dataclass
from functools import lru_cache
from heapq import heappush, heappop, heapify
from itertools import product
from typing import Callable, List

from utils.binary_search import binary_search


def ints(line):
    return [int(x) for x in line.split(' ')]


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

    monkeys = []
    for i in range(0, len(lines), 7):
        line = lines[i]
        assert line.startswith("Monkey")

        i += 1
        line = lines[i]
        items_raw = line.split(': ')[1]
        items = [int(x) for x in items_raw.split(', ')]

        i += 1
        line = lines[i]
        op_raw, num = line.split(' old ')[1].split()
        if op_raw == '*':
            if num == 'old':
                op = square()
            else:
                op = mul(int(num))
        elif op_raw == '+':
            if num == 'old':
                op = double()
            else:
                op = plus(int(num))
        else:
            raise ValueError(f'line: {line}')

        i += 1
        line = lines[i]
        assert ' divisible by ' in line, line
        div = int(line.split(' divisible by ')[1])

        true_target = int(lines[i+1].split(' monkey ')[1])
        false_target = int(lines[i+2].split(' monkey ')[1])

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

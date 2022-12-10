#!/usr/bin/env python
import functools
import sys
from collections import namedtuple, Counter, deque, defaultdict
from dataclasses import dataclass
from functools import lru_cache
from heapq import heappush, heappop, heapify
from itertools import product


def ints(line):
    return [int(x) for x in line.split(' ')]


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


def binary_search(items, target, fun):
    left = 0
    right = len(items)
    while left < right:
        mid = left + (right - left) // 2
        current = fun(mid)
        if target < current:
            right = mid
        else:
            left = mid + 1

    return items[left - 1]


def x_at(seq, c):
    def fun(index):
        return seq[index][0]

    _, x = binary_search(seq, c, fun)
    return x


def render_sprite(sprite):
    for start in range(0, 240, 40):
        print(''.join(sprite[start:start + 40]))


def solve(lines):
    cycles = 1
    x = 1
    seq = [(1, 0)]

    for line in lines:
        if line == 'noop':
            cycles += 1
        elif line.startswith('addx '):
            x += int(line.split()[1])
            cycles += 2
        else:
            raise ValueError(f"unexpected line: {line}")

        seq.append((cycles, x))

    sprite = []
    for c in range(240):
        x = x_at(seq, c + 1)
        c %= 40
        if abs(c - x) <= 1:
            sprite.append('#')
        else:
            sprite.append('.')

    render_sprite(sprite)


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines))


if __name__ == '__main__':
    main()

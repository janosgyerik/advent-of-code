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


def parse_num(s, start):
    x = 0
    i = start
    while i < len(s) and '0' <= s[i] <= '9':
        x *= 10
        x += ord(s[i]) - ord('0')
        i += 1
    return x


def parse_packets(line):
    root = []
    node = root
    stack = []
    i = 1
    while i < len(line) - 1:
        c = line[i]
        if c == '[':
            stack.append(node)
            node.append([])
            node = node[-1]
            i += 1
        elif c == ']':
            node = stack[-1]
            stack = stack[:-1]
            i += 1
        elif c == ',':
            i += 1
        else:
            num = parse_num(line, i)
            node.append(num)
            i += len(str(num))

    return root


def parse_pairs(lines):
    for start in range(0, len(lines), 3):
        left = parse_packets(lines[start])
        right = parse_packets(lines[start + 1])
        yield left, right


def cmp(left, right):
    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return 0
        if left < right:
            return -1
        return 1

    if isinstance(left, list) and isinstance(right, list):
        for a, b in zip(left, right):
            x = cmp(a, b)
            if x < 0:
                return -1
            if 0 < x:
                return 1

        return cmp(len(left), len(right))

    if isinstance(left, int):
        return cmp([left], right)

    return cmp(left, [right])


def solve(lines):
    count = 0
    index = 1
    for left, right in parse_pairs(lines):
        if cmp(left, right) < 0:
            print(index)
            count += index

        index += 1

    return count


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines))


if __name__ == '__main__':
    main()

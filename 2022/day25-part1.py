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
from utils import grids


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


def parse_and_solve(lines, *args):
    input_ = parse_input(lines)
    return solve(input_)


def main():
    lines = read_lines(sys.argv[1])
    print(parse_and_solve(lines, *(sys.argv[2:])))


@dataclass
class Foo:
    pass


@dataclass
class Input:
    lines: List[str]


def parse_input(lines):
    return Input(lines)


def snafu_to_dec(line):
    dec = 0
    m = 1
    for c in line[::-1]:
        if c == '=':
            dec -= m * 2
        elif c == '-':
            dec -= m
        else:
            dec += m * int(c)

        m *= 5

    return dec


def dec_to_snafu(dec):
    """
    >>> dec_to_snafu(124)
    '10-'

    >>> dec_to_snafu(198)
    '2=0='

    """
    snafu = []
    work = dec
    while work:
        div, mod = divmod(work, 5)
        if mod < 3:
            snafu.append(mod)
            work = div
        elif mod == 3:
            snafu.append('=')
            work = div + 1
        else:
            snafu.append('-')
            work = div + 1

    return ''.join(str(c) for c in reversed(snafu))


def solve(input_):
    total = sum(snafu_to_dec(line) for line in input_.lines)
    return total, dec_to_snafu(total)


if __name__ == '__main__':
    main()

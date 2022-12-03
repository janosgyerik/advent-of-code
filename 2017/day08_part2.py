#!/usr/bin/env python
import math

import utils
import re
from collections import namedtuple, Counter, deque, defaultdict
from itertools import product
from heapq import heappush, heappop, heapify
from functools import lru_cache
from dataclasses import dataclass


@dataclass
class Op:
    reg: str
    name: str
    value: int


def create_op(parts):
    assert(len(parts)) == 3
    return Op(parts[0], parts[1], int(parts[2]))


@dataclass
class Cond:
    reg: str
    op: str
    value: int


def create_cond(parts):
    assert(len(parts)) == 3
    return Cond(parts[0], parts[1], int(parts[2]))


def evaluate(registers, cond):
    register_value = registers[cond.reg]

    if cond.op == '<':
        return register_value < cond.value
    if cond.op == '>':
        return register_value > cond.value
    if cond.op == '<=':
        return register_value <= cond.value
    if cond.op == '>=':
        return register_value >= cond.value
    if cond.op == '==':
        return register_value == cond.value
    if cond.op == '!=':
        return register_value != cond.value

    assert False, f'unsupported operator: {cond.op}'


def apply(registers, op):
    if op.name == 'inc':
        registers[op.reg] += op.value
    elif op.name == 'dec':
        registers[op.reg] -= op.value
    else:
        assert False, f'unsupported operation: {op.name}'


def solve(lines):
    registers = defaultdict(int)
    highest = 0

    for line in lines:
        left, right = line.split(' if ')
        op = create_op(left.split())
        cond = create_cond(right.split())
        if evaluate(registers, cond):
            apply(registers, op)
            highest = max(highest, registers[op.reg])

    return highest


if __name__ == '__main__':
    utils.solve(solve)

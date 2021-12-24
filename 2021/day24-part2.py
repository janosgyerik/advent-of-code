#!/usr/bin/env python
import math
from numbers import Number
from typing import Callable, Any

import utils
import re
from collections import namedtuple, Counter, deque, defaultdict
from itertools import product
from heapq import heappush, heappop, heapify
from functools import lru_cache
import utils

varmap = {c: i for i, c in enumerate("wxyz")}


class Machine:
    def __init__(self, instructions):
        self.instructions = [self._parse_instruction(s)
                             for s in instructions
                             if not s.startswith('#')]
        self.vars = None
        self.inputs = None
        self.reset()

    def reset(self):
        self.vars = [0] * 4

    def execute(self, inputs):
        self.reset()
        self.inputs = list(reversed(inputs))
        for inst in self.instructions:
            inst()
        return self.vars[-1]

    def _inp(self, dest):
        def fun():
            assert self.inputs, "not enough inputs!"
            self.vars[dest] = self.inputs.pop()

        return fun

    def _eval(self, arg):
        if arg.isalpha():
            return self.vars[varmap[arg]]

        return int(arg)

    def _mul(self, dest, arg):
        def fun():
            self.vars[dest] *= self._eval(arg)

        return fun

    def _div(self, dest, arg):
        def fun():
            arg2 = self._eval(arg)
            assert arg2 != 0
            self.vars[dest] //= arg2

        return fun

    def _mod(self, dest, arg):
        def fun():
            assert self.vars[dest] >= 0
            arg2 = self._eval(arg)
            assert arg2 > 0
            self.vars[dest] %= arg2

        return fun

    def _add(self, dest, arg):
        def fun():
            self.vars[dest] += self._eval(arg)

        return fun

    def _eql(self, dest, arg):
        def fun():
            self.vars[dest] = int(self.vars[dest] == self._eval(arg))

        return fun

    def _parse_instruction(self, s):
        args = s.split()
        if len(args) == 2:
            inp, varname = args
            assert inp == 'inp'
            assert varname.isalpha()
            return self._inp(varmap[varname])

        assert len(args) == 3

        op, dest, arg = args
        assert not dest.isnumeric()

        if op == 'add':
            return self._add(varmap[dest], arg)

        if op == 'mul':
            return self._mul(varmap[dest], arg)

        if op == 'div':
            return self._div(varmap[dest], arg)

        if op == 'mod':
            return self._mod(varmap[dest], arg)

        if op == 'eql':
            return self._eql(varmap[dest], arg)

        raise ValueError("not implemented:", s)


def execute(m, digits):
    print(''.join(str(c) for c in digits))
    return m.execute(digits)


def solve(lines):
    m = Machine(lines)
    # 0 1 2 3 4 5 6 7 8 9
    # 5 4 9 2 9 9 9 5 9 7
    # a0 + 2 == a9
    # a1 + 5 == a8
    # a2 == a5
    # a3 + 7 == a4
    # a6 - 4 == a7
    # a10 - 6 == a11
    # a12 + 1 == a13
    #                  0  1  2  3  4  5  6  7  8  9
    return execute(m, [1, 1, 1, 1, 8, 1, 5, 1, 6, 3, 7, 1, 1, 2])


if __name__ == '__main__':
    utils.solve(solve)

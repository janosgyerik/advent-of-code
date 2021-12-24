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

    def _mul_literal(self, dest, arg):
        def fun():
            self.vars[dest] *= arg

        return fun

    def _mul_var(self, dest, index):
        def fun():
            self.vars[dest] *= self.vars[index]

        return fun

    def _div_literal(self, dest, arg):
        assert arg != 0

        def fun():
            self.vars[dest] //= arg

        return fun

    def _div_var(self, dest, index):
        def fun():
            assert self.vars[index] != 0
            self.vars[dest] //= self.vars[index]

        return fun

    def _mod_literal(self, dest, arg):
        assert arg > 0

        def fun():
            self.vars[dest] %= arg

        return fun

    def _mod_var(self, dest, index):
        def fun():
            assert self.vars[dest] >= 0
            assert self.vars[index] > 0
            self.vars[dest] %= self.vars[index]

        return fun

    def _add_literal(self, dest, arg):
        def fun():
            self.vars[dest] += arg

        return fun

    def _add_var(self, dest, index):
        def fun():
            self.vars[dest] += self.vars[index]

        return fun

    def _eql_literal(self, dest, arg):
        def fun():
            self.vars[dest] = int(self.vars[dest] == arg)

        return fun

    def _eql_var(self, dest, index):
        def fun():
            self.vars[dest] = int(self.vars[dest] == self.vars[index])

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
            if arg.isalpha():
                return self._add_var(varmap[dest], varmap[arg])
            else:
                return self._add_literal(varmap[dest], int(arg))

        if op == 'mul':
            if arg.isalpha():
                return self._mul_var(varmap[dest], varmap[arg])
            else:
                return self._mul_literal(varmap[dest], int(arg))

        if op == 'div':
            if arg.isalpha():
                return self._div_var(varmap[dest], varmap[arg])
            else:
                return self._div_literal(varmap[dest], int(arg))

        if op == 'mod':
            if arg.isalpha():
                return self._mod_var(varmap[dest], varmap[arg])
            else:
                return self._mod_literal(varmap[dest], int(arg))

        if op == 'eql':
            if arg.isalpha():
                return self._eql_var(varmap[dest], varmap[arg])
            else:
                return self._eql_literal(varmap[dest], int(arg))

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

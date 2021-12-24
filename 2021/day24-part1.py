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
        self.instructions = [self._parse_instruction(s) for s in instructions if not s.startswith('#')]
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


def counter_up(digits, end):
    index = end

    while True:
        if digits[index] == 9:
            digits[index] = 1
            index -= 1

        else:
            digits[index] += 1
            index = end
            yield digits


def counter_down(digits, end):
    index = end

    while True:
        if digits[index] == 1:
            digits[index] = 9
            index -= 1

        else:
            digits[index] -= 1
            index = end
            yield digits


def crack1(m):
    """
[9, 4, 9, 2, 9, 9, 9, 5, 9, 7, 9, 7, 8, 9]
[9, 0, 0, 354]
[9, 4, 9, 2, 9, 9, 9, 5, 9, 7, 9, 5, 8, 9]
[9, 0, 0, 352]
[9, 4, 9, 2, 9, 9, 9, 5, 9, 7, 9, 3, 8, 9]
[9, 0, 0, 13]
[9, 4, 9, 2, 9, 9, 9, 5, 9, 5, 9, 3, 8, 9]
[9, 0, 0, 11]
[9, 4, 9, 2, 9, 9, 9, 5, 9, 3, 9, 3, 8, 9]
[9, 0, 0, 9]
[9, 4, 9, 2, 9, 9, 9, 5, 9, 1, 9, 3, 8, 9]
[9, 0, 0, 7]
    """
    digits = [9, 4, 9, 2, 9, 9, 9, 5, 9, 3, 9, 3, 8, 9]
    digits = [9, 4, 9, 2, 9, 9, 9, 5, 9, 3, 9, 3, 8, 9]
    counter = counter_down(digits)
    lowest = float('inf')
    for _ in range(100000000):
        monad = next(counter)
        result = m.execute(monad)
        if result[-1] < lowest:
            lowest = result[-1]
            print(monad)
            print(result)

        if result[-1] == 0:
            print('solved!')
            print(monad)
            print(result)
            print(''.join(str(c) for c in monad))
            break


class MonadCounter:
    def __init__(self, digits=None):
        if digits is None:
            self.digits = [9] * 14
        else:
            self.digits = digits[:]
        self.end = len(self.digits) - 1

    def dec(self):
        index = self.end
        while self.digits[index] == 1:
            self.digits[index] = 9
            index -= 1

        self.digits[index] -= 1


def crack2(m):
    counter = MonadCounter()
    lowest = float('inf')
    # [9, 4, 9, 2, 9, 9, 9, 5, 9, 1, 9, 3, 8, 9]
    for _ in range(100000):
        monad = counter.digits
        result = m.execute(monad)
        if result[-1] < lowest - 1:
            lowest = result[-1]
            print(monad)
            print(result)
            counter.end -= 1

        if result[-1] == 0:
            print('solved!')
            print(monad)
            print(result)
            print(''.join(str(c) for c in monad))
            break

        counter.dec()


def crack3(m):
    digits = [9] * 14
    digits = [9, 4, 9, 2, 9, 9, 9, 5, 9, 1, 9, 3, 8, 9]
    new_digits = digits
    smallest = m.execute(digits)[-1]

    for _ in range(10):
        for index in range(14):
            old = digits[index]
            if digits[index] > 1:
                digits[index] -= 1
                result = m.execute(digits)[-1]
                if result < smallest:
                    smallest = result
                    print(result, digits)
                    new_digits = digits[:]
                digits[index] = old

            if digits[index] > 2:
                digits[index] -= 2
                result = m.execute(digits)[-1]
                if result < smallest:
                    smallest = result
                    print(result, digits)
                    new_digits = digits[:]
                digits[index] = old

            if digits[index] < 9:
                digits[index] += 1
                result = m.execute(digits)[-1]
                if result < smallest:
                    smallest = result
                    print(result, digits)
                    new_digits = digits[:]
                digits[index] = old

            if digits[index] < 8:
                digits[index] += 2
                result = m.execute(digits)[-1]
                if result < smallest:
                    smallest = result
                    print(result, digits)
                    new_digits = digits[:]
                digits[index] = old

        if digits == new_digits:
            break

        digits = new_digits


def crack4(m):
    digits = [9, 4, 9, 2, 9, 9, 9, 5, 9, 1, 9, 3, 8, 9]
    digits = [9] * 14
    digits = [int(c) for c in '54929995979389']
    smallest = m.execute(digits)[-1]
    print(smallest)

    for index in range(14):
        old = digits[index]
        for alt in range(1, 10):
            if alt == old:
                continue

            digits[index] = alt
            value = m.execute(digits)[-1]
            print(value, digits)

        digits[index] = old


def crack5(m):
    """
[9, 4, 9, 2, 9, 9, 9, 5, 9, 7, 9, 7, 8, 9]
[9, 0, 0, 354]
[9, 4, 9, 2, 9, 9, 9, 5, 9, 7, 9, 5, 8, 9]
[9, 0, 0, 352]
[9, 4, 9, 2, 9, 9, 9, 5, 9, 7, 9, 3, 8, 9]
[9, 0, 0, 13]
[9, 4, 9, 2, 9, 9, 9, 5, 9, 5, 9, 3, 8, 9]
[9, 0, 0, 11]
[9, 4, 9, 2, 9, 9, 9, 5, 9, 3, 9, 3, 8, 9]
[9, 0, 0, 9]
[9, 4, 9, 2, 9, 9, 9, 5, 9, 1, 9, 3, 8, 9]
[9, 0, 0, 7]
    """
    digits = [9, 4, 9, 2, 9, 9, 9, 5, 9, 3, 9, 3, 8, 9]
    digits = [9, 4, 9, 2, 9, 9, 9, 5, 9, 1, 9, 3, 8, 9]
    counter = MonadCounter(digits)
    for _ in range(10):
        monad = counter.digits
        result = m.execute(monad)[-1]
        print(monad)
        print(result)
        counter.dec()


def crack_single(m, digits):
    print(digits, ''.join(str(c) for c in digits))
    result = m.execute(digits)
    print(result)


def crack6(m):
    # crack1(m)
    # crack2(m)
    # crack3(m)
    # crack4(m)
    # crack2(m)
    digits = [9] * 14
    digits[-2] = 8
    # digits = [9, 9, 9, 2, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
    # digits = [9, 9, 9, 2, 9, 9, 9, 5, 1, 9, 9, 9, 9, 9]
    # digits = [9, 9, 9, 2, 9, 9, 9, 5, 1, 1, 8, 9, 9, 9]
    # digits = [9, 9, 9, 2, 9, 9, 9, 5, 1, 1, 8, 9, 8, 9]
    # digits[-1] must be digits[-2] + 1
    digits = [9, 9, 9, 2, 9, 9, 9, 9, 9, 9, 9, 9, 8, 9]
    digits = [9, 9, 9, 2, 9, 9, 9, 5, 9, 9, 9, 9, 8, 9]
    digits = [9, 9, 9, 2, 9, 9, 9, 5, 9, 1, 8, 9, 8, 9]
    start = 6
    low = m.execute(digits)
    for i in range(9, 0, -1):
        for j in range(9, 0, -1):
            b1, b2 = digits[start:start + 2]
            digits[start] = i
            digits[start + 1] = j
            result = m.execute(digits)
            if result < low:
                print(result, digits)
                low = result

            digits[start] = b1
            digits[start + 1] = b2


def crack7(m):
    start = [9, 9, 9, 2, 9, 9, 9, 9, 9, 9, 9, 9, 8, 9]
    start = [9, 9, 9, 2, 9, 9, 9, 5, 9, 1, 9, 3, 8, 9]
    start = [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 3, 8, 9]
    #23 [9, 9, 9, 2, 9, 2, 9, 5, 9, 5, 9, 3, 8, 9]
    # when digit[12] + 1 == digit[13] -> contributes 0 -> end with 89
    # when digit[10] - 6 == digit[11] -> contributes 0 -> 93
    # when  digit[6] - 4 == digit[7]  -> contributes 0 -> 95
    # when  digit[3] + 7 == digit[4]  -> contributes 0 -> 29
    # digit[3] + 7 must be digit[4] -> contributes smallest
    counter = counter_down(start, 9)

    low = m.execute(start)
    print(low, start)

    limit = 10000000
    for i in range(limit):
        digits = next(counter)
        result = m.execute(digits)
        if i % (limit // 100) == 0:
            print('checkpoint', result, digits)
        if result < low:
            low = result
            print(result, digits)
            if low == 0:
                break


def solve(lines):
    m = Machine(lines)
    # crack7(m)
    # 0 1 2 3 4 5 6 7 8 9
    # 5 4 9 2 9 9 9 5 9 7
    crack_single(m, [5, 4, 9, 2, 9, 9, 9, 5, 9, 7, 9, 3, 8, 9])
    crack_single(m, [7, 4, 9, 2, 9, 9, 9, 5, 9, 9, 9, 3, 8, 9])


if __name__ == '__main__':
    utils.solve(solve)

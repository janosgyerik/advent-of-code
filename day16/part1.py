#!/usr/bin/env python

import sys, re
from collections import namedtuple

re_ints = re.compile(r'\d+')

Instruction = namedtuple('Instruction', ['opcode', 'a', 'b', 'c'])
Case = namedtuple('Case', ['before', 'instruction', 'after'])


class Machine:
    def __init__(self):
        self.reg = [0] * 4

    def addr(self, a, b, c):
        self.reg[c] = self.reg[a] + self.reg[b]

    def addi(self, a, b, c):
        self.reg[c] = self.reg[a] + b

    def mulr(self, a, b, c):
        self.reg[c] = self.reg[a] * self.reg[b]

    def muli(self, a, b, c):
        self.reg[c] = self.reg[a] * b

    def banr(self, a, b, c):
        self.reg[c] = self.reg[a] & self.reg[b]

    def bani(self, a, b, c):
        self.reg[c] = self.reg[a] & b

    def borr(self, a, b, c):
        self.reg[c] = self.reg[a] | self.reg[b]

    def bori(self, a, b, c):
        self.reg[c] = self.reg[a] | b

    def setr(self, a, b, c):
        self.reg[c] = self.reg[a]

    def seti(self, a, b, c):
        self.reg[c] = a

    def gtir(self, a, b, c):
        self.reg[c] = 1 if a > self.reg[b] else 0

    def gtri(self, a, b, c):
        self.reg[c] = 1 if self.reg[a] > b else 0

    def gtrr(self, a, b, c):
        self.reg[c] = 1 if self.reg[a] > self.reg[b] else 0

    def eqir(self, a, b, c):
        self.reg[c] = 1 if a == self.reg[b] else 0

    def eqri(self, a, b, c):
        self.reg[c] = 1 if self.reg[a] == b else 0

    def eqrr(self, a, b, c):
        self.reg[c] = 1 if self.reg[a] == self.reg[b] else 0

    def ops(self):
        return (
                self.addr, self.addi,
                self.mulr, self.muli,
                self.banr, self.bani,
                self.borr, self.bori,
                self.setr, self.seti,
                self.gtir, self.gtri, self.gtrr,
                self.eqir, self.eqri, self.eqrr,
                )

    def behaves_like_3_opcodes(self, case):
        count = 0
        for op in self.ops():
            self.reg = case.before[:]
            op(case.instruction.a, case.instruction.b, case.instruction.c)
            if self.reg == case.after:
                count += 1
                if count >= 3:
                    return True

        return False


def ints(line):
    return [int(x) for x in re_ints.findall(line)]


def parse_cases(lines):
    for i in range(0, len(lines), 4):
        raw_before = lines[i]
        raw_instruction = lines[i + 1]
        raw_after = lines[i + 2]

        if not raw_before.startswith('Before:'):
            # end of samples
            break

        yield Case(ints(raw_before), Instruction(*ints(raw_instruction)), ints(raw_after))


if __name__ == '__main__':
    m = Machine()
    for case in parse_cases(sys.stdin.readlines()):
        if m.behaves_like_3_opcodes(case):
            print(case)

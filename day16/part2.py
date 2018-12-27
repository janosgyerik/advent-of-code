#!/usr/bin/env python

import sys, re
from collections import namedtuple

re_ints = re.compile(r'\d+')

Instruction = namedtuple('Instruction', ['opcode', 'a', 'b', 'c'])
Case = namedtuple('Case', ['before', 'instruction', 'after'])


class Machine:
    def __init__(self):
        self.reset()

    def reset(self):
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

    def ops_list(self):
        return (
                self.addr, self.addi,
                self.mulr, self.muli,
                self.banr, self.bani,
                self.borr, self.bori,
                self.setr, self.seti,
                self.gtir, self.gtri, self.gtrr,
                self.eqir, self.eqri, self.eqrr,
                )

    def find_new_opcode(self, cases, ops):
        for case in cases:
            inst = case.instruction
            single_op = None
            for op in ops:
                self.reg = case.before[:]
                op(inst.a, inst.b, inst.c)
                if self.reg == case.after:
                    if single_op:
                        single_op = None
                        break
                    single_op = op

            if single_op:
                return inst.opcode, single_op

        raise RuntimeError('Could not find new clearly identifiable opcode')

    def compute_opcodes(self, cases):
        self.ops = {}

        undecided_cases = cases
        undecided_ops = list(self.ops_list())

        while len(self.ops) != 16:
            opcode, op = self.find_new_opcode(undecided_cases, undecided_ops)
            self.ops[opcode] = op
            undecided_cases = [x for x in undecided_cases if x.instruction.opcode != opcode]
            undecided_ops.remove(op)

    def execute(self, instructions):
        self.reset()
        for inst in instructions:
            self.ops[inst.opcode](inst.a, inst.b, inst.c)


def ints(line):
    return [int(x) for x in re_ints.findall(line)]


def parse_cases_and_instructions(lines):
    cases = []
    instructions = []

    for i in range(0, len(lines), 4):
        raw_before = lines[i]
        raw_instruction = lines[i + 1]
        raw_after = lines[i + 2]

        if not raw_before.startswith('Before:'):
            break

        case = Case(ints(raw_before), Instruction(*ints(raw_instruction)), ints(raw_after))
        cases.append(case)

    for i in range(i + 2, len(lines)):
        instructions.append(Instruction(*ints(lines[i])))

    return cases, instructions

if __name__ == '__main__':
    cases, instructions = parse_cases_and_instructions(sys.stdin.readlines())
    m = Machine()
    m.compute_opcodes(cases)
    m.execute(instructions)
    print(m.reg[0])

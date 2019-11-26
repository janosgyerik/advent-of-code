#!/usr/bin/env python

import sys, re
from collections import namedtuple

re_ints = re.compile(r'\d+')

Instruction = namedtuple('Instruction', ['fun', 'a', 'b', 'c'])


class Machine:
    def __init__(self, ip, instructions):
        self.funs = {
                'addr': self.addr,
                'addi': self.addi,
                'mulr': self.mulr,
                'muli': self.muli,
                'banr': self.banr,
                'bani': self.bani,
                'borr': self.borr,
                'bori': self.bori,
                'setr': self.setr,
                'seti': self.seti,
                'gtir': self.gtir,
                'gtri': self.gtri,
                'gtrr': self.gtrr,
                'eqir': self.eqir,
                'eqri': self.eqri,
                'eqrr': self.eqrr,
                }
        self.ip = ip
        self.instructions = self.convert(instructions)
        self.reset()
        self.seen = set()

    def convert(self, instructions):
        return [Instruction(self.funs[x.fun], x.a, x.b, x.c) for x in instructions]

    def reset(self):
        self.reg = [0] * 6

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
        # see input.txt why...
        v = self.reg[4]
        if v in self.seen:
            sys.exit(1)
        self.seen.add(v)
        print(v)
        self.reg[c] = 1 if self.reg[a] == self.reg[b] else 0

    def execute(self, interactive=False):
        while True:
            index = self.reg[self.ip]
            if index >= len(self.instructions):
                break

            inst = self.instructions[index]
            inst.fun(inst.a, inst.b, inst.c)
            self.reg[self.ip] += 1
            #print(inst, self.reg)

            if interactive:
                sys.stdin.readline()


def ints(line):
    return [int(x) for x in re_ints.findall(line)]


def machine_from_lines(lines):
    ip = int(lines[0][4])
    instructions = []

    for line in lines[1:]:
        name, args = line.split(' ', 1)
        instructions.append(Instruction(name, *ints(args)))

    return Machine(ip, instructions)

if __name__ == '__main__':
    start = int(sys.argv[1])
    with open(sys.argv[2]) as fh:
        lines = fh.readlines()
    m = machine_from_lines(lines)
    m.reg[0] = start
    m.execute()

#!/usr/bin/env python

import sys
from collections import namedtuple

Instruction = namedtuple('Instruction', ['fun', 'arg'])


class Machine:
    def __init__(self, ip, instructions):
        self.funs = {
            'nop': self.nop,
            'acc': self.acc,
            'jmp': self.jmp,
        }
        self.ip = ip
        self.instructions = self.convert(instructions)
        self.reset()

    def convert(self, instructions):
        return [Instruction(self.funs[x.fun], x.arg) for x in instructions]

    def reset(self):
        self.ip = 0
        self.accumulator = 0

    def nop(self, arg):
        self.ip += 1

    def acc(self, arg):
        self.accumulator += arg
        self.ip += 1

    def jmp(self, arg):
        self.ip += arg

    def execute(self):
        used = set()
        while self.ip not in used:
            if self.ip >= len(self.instructions):
                return True
            used.add(self.ip)
            inst = self.instructions[self.ip]
            inst.fun(inst.arg)

        return False


def ints(line):
    return [int(x) for x in line.split(' ')]


def machine_from_lines(ip, lines):
    instructions = []

    for line in lines:
        name, args = line.split(' ', 1)
        instructions.append(Instruction(name, *ints(args)))

    return Machine(ip, instructions)


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


def main():
    start = int(sys.argv[1])
    lines = read_lines(sys.argv[2])
    m = machine_from_lines(start, lines)
    m.execute()
    print(m.accumulator)

    for index, line in enumerate(lines):
        if line.startswith('nop') or line.startswith('jmp'):
            orig = m.instructions[index]
            rfun = 'nop' if line.startswith('jmp') else 'jmp'
            fix = Instruction(m.funs[rfun], orig.arg)
            m.instructions[index] = fix
            m.reset()
            if m.execute():
                print(m.accumulator)
                break
            m.instructions[index] = orig


if __name__ == '__main__':
    main()

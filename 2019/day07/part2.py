#!/usr/bin/env python3

import sys

from itertools import permutations
from collections import deque


class Machine:
    def __init__(self, memory):
        self.funs = {
            1: lambda: self.bi_func(lambda x, y: x + y),
            2: lambda: self.bi_func(lambda x, y: x * y),
            3: lambda: self.input(),
            4: lambda: self.output(),
            5: lambda: self.jump_if_true(),
            6: lambda: self.jump_if_false(),
            7: lambda: self.less_than(),
            8: lambda: self.equals(),
            99: lambda: self.stop(),
        }
        self.backup = memory[:]
        self.reset()

    def reset(self):
        self.halted = False
        self.paused = False
        self.waiting_on_input = False
        self.ip = 0
        self.memory = self.backup[:]
        self.inputs = []
        self.inputs_i = 0
        self.out1 = 0

    def copy(self):
        return Machine(self.backup)

    def stop(self):
        self.halted = True

    def set(self, index, value):
        self.memory[index] = value

    def get(self, index=None):
        return self.memory[index] if index else self.memory[self.ip]

    def argi(self, pos=0):
        return self.memory[self.ip + pos]

    def argr(self, pos):
        return self.memory[self.argi(pos)]

    def arg(self, pos):
        mode = self.argi() // (10 ** (pos + 1)) % 10
        return self.argi(pos) if mode else self.argr(pos)

    def input(self):
        if self.inputs_i == len(self.inputs):
            self.paused = True
            self.waiting_on_input = True
            return
        self.set(self.argi(1), self.inputs[self.inputs_i])
        self.inputs_i += 1
        self.ip += 2

    def output(self):
        self.out1 = self.arg(1)
        self.ip += 2
        self.paused = True

    def bi_func(self, fun):
        s1 = self.arg(1)
        s2 = self.arg(2)
        self.set(self.argi(3), fun(s1, s2))
        self.ip += 4

    def jump_if_true(self):
        if self.arg(1):
            self.ip = self.arg(2)
        else:
            self.ip += 3

    def jump_if_false(self):
        if not self.arg(1):
            self.ip = self.arg(2)
        else:
            self.ip += 3

    def less_than(self):
        if self.arg(1) < self.arg(2):
            v = 1
        else:
            v = 0
        self.set(self.argi(3), v)
        self.ip += 4

    def equals(self):
        if self.arg(1) == self.arg(2):
            v = 1
        else:
            v = 0
        self.set(self.argi(3), v)
        self.ip += 4

    def execute(self):
        self.paused = False
        self.waiting_on_input = False
        while not self.halted and not self.paused:
            opcode = self.get() % 100
            self.funs[opcode]()


def ints(line):
    return [int(x) for x in line.rstrip().split(',')]


def combinations(phases):
    yield from permutations(phases)


def compute_output(prototype, phases):
    machines = deque()
    for phase in phases:
        copy = prototype.copy()
        copy.inputs.append(phase)
        machines.append(copy)

    while any(map(lambda x: not x.halted, machines)):
        machines[0].inputs.append(machines[-1].out1)
        machines[0].execute()

        if machines[0].waiting_on_input:
            machines.rotate(1)
        else:
            machines.rotate(-1)

    return machines[-1].out1


def main():
    m = Machine(ints(sys.stdin.readlines()[0]))
    print(max(compute_output(m, c) for c in combinations(range(5, 10))))


if __name__ == '__main__':
    main()

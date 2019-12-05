#!/usr/bin/env python3

import sys


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
        self.backup = memory
        self.reset()

    def reset(self):
        self.terminate = False
        self.ip = 0
        self.memory = self.backup[:]
        self.in1 = 0
        self.out1 = 0
        self.outputs = []

    def stop(self):
        self.terminate = True

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
        self.set(self.argi(1), self.in1)
        self.ip += 2

    def output(self):
        self.out1 = self.arg(1)
        self.ip += 2
        self.outputs.append(self.out1)

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

    def execute(self, in1):
        self.in1 = in1
        while not self.terminate:
            opcode = self.get() % 100
            self.funs[opcode]()


def ints(line):
    return [int(x) for x in line.rstrip().split(',')]


def main():
    m = Machine(ints(sys.stdin.readlines()[0]))
    m.execute(5)
    print(m.out1)


if __name__ == '__main__':
    main()

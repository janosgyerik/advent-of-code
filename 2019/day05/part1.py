#!/usr/bin/env python

import re
import sys

re_ints = re.compile(r'\d+')

EXIT = 99


class Machine:
    def __init__(self, memory):
        self.funs = {
            1: lambda z: self.bi_func(z, lambda x, y: x + y),
            2: lambda z: self.bi_func(z, lambda x, y: x * y),
            3: lambda z: self.input,
            4: lambda z: self.output,
        }
        self.backup = memory
        self.reset()

    def reset(self):
        self.ip = 0
        self.memory = self.backup[:]
        self.arg1 = None
        self.out1 = None

    def set(self, index, value):
        self.memory[index] = value

    def get(self, index):
        return self.memory[index]

    def input(self):
        print(f"store at {self.memory[self.ip+1]} the value {self.arg1}")
        self.memory[self.memory[self.ip + 1]] = self.arg1
        self.ip += 2

    def output(self):
        self.out1 = self.memory[self.memory[self.ip + 1]]
        self.ip += 2

    def arg(self, pos):
        mode = self.memory[self.ip] // (10 ** (pos + 1)) % 10
        value = self.memory[self.ip + pos]
        return value if mode else self.memory[value]

    def bi_func(self, z, fun):
        s1 = self.arg(1)
        s2 = self.arg(2)
        # s1 = self.memory[self.memory[self.ip + 1]]
        # s2 = self.memory[self.memory[self.ip + 2]]
        self.memory[self.memory[self.ip + 3]] = fun(s1, s2)
        self.ip += 4

    def execute(self, arg1):
        self.arg1 = arg1
        while self.ip < len(self.memory):
            z = self.memory[self.ip]
            if z == EXIT:
                return

            opcode = z % 100
            self.funs[opcode](z)
            break


def ints(line):
    return [int(x) for x in re_ints.findall(line)]


def main():
    m = Machine(ints(sys.stdin.readlines()[0]))
    m.execute(1)
    print(m.out1)


if __name__ == '__main__':
    main()

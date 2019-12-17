#!/usr/bin/env python3

import sys

from collections import defaultdict


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
            9: lambda: self.update_relbase(),
            99: lambda: self.stop(),
        }
        self.backup = defaultdict(lambda: 0, {i: v for i, v in enumerate(memory)})
        self.reset()

    def reset(self):
        self.halted = False
        self.paused = False
        self.waiting_on_input = False
        self.ip = 0
        self.memory = self.backup.copy()
        self.inputs = []
        self.inputs_i = 0
        self.out1 = 0
        self.outputs = []
        self.relbase = 0

    def copy(self):
        return Machine(self.backup)

    def stop(self):
        self.halted = True

    def set(self, index, value):
        self.memory[index] = value

    def addrr(self, pos):
        return self.argi(pos)

    def addrp(self, pos):
        return self.addrr(pos) + self.relbase

    def addr(self, pos):
        mode = self.mode(pos)
        if mode == 0:
            return self.addrr(pos)
        elif mode == 2:
            return self.addrp(pos)

        raise ValueError(f'invalid address mode: {mode}')

    def argi(self, pos=0):
        return self.memory[self.ip + pos]

    def argr(self, pos):
        return self.memory[self.addrr(pos)]

    def argp(self, pos):
        return self.memory[self.addrp(pos)]

    def arg(self, pos):
        mode = self.mode(pos)
        if mode == 1:
            return self.argi(pos)
        elif mode == 0:
            return self.argr(pos)
        elif mode == 2:
            return self.argp(pos)

        raise ValueError(f'unknown arg mode: {mode}')

    def mode(self, pos):
        return self.argi() // (10 ** (pos + 1)) % 10

    def input(self):
        if self.inputs_i == len(self.inputs):
            self.paused = True
            self.waiting_on_input = True
            return

        self.set(self.addr(1), self.inputs[self.inputs_i])
        self.inputs_i += 1
        self.ip += 2

    def output(self):
        self.out1 = self.arg(1)
        self.outputs.append(self.out1)
        self.ip += 2
        self.paused = True

    def bi_func(self, fun):
        self.set(self.addr(3), fun(self.arg(1), self.arg(2)))
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
        self.set(self.addr(3), int(self.arg(1) < self.arg(2)))
        self.ip += 4

    def equals(self):
        self.set(self.addr(3), int(self.arg(1) == self.arg(2)))
        self.ip += 4

    def update_relbase(self):
        self.relbase += self.arg(1)
        self.ip += 2

    def execute(self):
        self.paused = False
        self.waiting_on_input = False
        while not self.halted and not self.paused:
            opcode = self.memory[self.ip] % 100
            self.funs[opcode]()


class Grid:
    def __init__(self):
        self.grid = {}
        self.min_x = 0
        self.min_y = 0
        self.max_x = 0
        self.max_y = 0
        self.scaffolds = set()

    def add(self, x, y, c):
        self.grid[(x, y)] = c
        self.max_x = max(self.max_x, x)
        self.max_y = max(self.max_y, y)
        if c == '#':
            self.scaffolds.add((x, y))

    def compute_alignment_params(self):
        return sum(x * y for x, y in self.intersections())

    def intersections(self):
        for x, y in self.scaffolds:
            if self.is_intersection(x, y):
                yield x, y

    def is_intersection(self, x, y):
        return all(p in self.scaffolds for p in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)])

    def display(self):
        for y in range(self.max_y + 1):
            for x in range(self.max_x + 1):
                print(self.grid[(x, y)], end='')
            print()


def ints(line):
    return [int(x) for x in line.split(',')]


def main():
    m = Machine(ints(sys.stdin.read().rstrip()))

    grid = Grid()
    x, y = 0, 0
    while not m.halted:
        m.execute()
        c = chr(m.out1)
        if m.out1 == 10:
            x = 0
            y += 1
        else:
            grid.add(x, y, c)
            x += 1

    grid.display()
    print(grid.compute_alignment_params())


if __name__ == '__main__':
    main()

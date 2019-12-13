#!/usr/bin/env python3

import sys

from collections import defaultdict, deque


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


def ints(line):
    return [int(x) for x in line.rstrip().split(',')]


class Grid:
    def __init__(self):
        self.grid = defaultdict(lambda: 0)
        self.pos = [0, 0]
        self.directions = deque([(0, 1), (1, 0), (0, -1), (-1, 0)])

    def direction(self):
        return self.directions[0]

    def visited(self):
        return len(self.grid)

    def paint_rotate_and_move(self, color, rotation):
        self.grid[tuple(self.pos)] = color
        if rotation == 0:
            self.turn_left()
        else:
            self.turn_right()
        self.advance()

    def color(self):
        return self.grid[tuple(self.pos)]

    def rotate(self, steps):
        self.directions.rotate(steps)

    def turn_left(self):
        self.rotate(-1)

    def turn_right(self):
        self.rotate(1)

    def advance(self):
        self.pos[0] += self.direction()[0]
        self.pos[1] += self.direction()[1]


def main():
    m = Machine(ints(sys.stdin.readlines()[0]))
    m.inputs = [0]
    g = Grid()
    while not m.halted:
        m.execute()
        m.execute()
        color, rotation = m.outputs[-2:]
        g.paint_rotate_and_move(color, rotation)
        m.inputs.append(g.color())

    print(g.visited())


if __name__ == '__main__':
    main()

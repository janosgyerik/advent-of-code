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


class Game:
    def __init__(self):
        self.mapping = ' #.-o'
        self.grid = {}
        self.ball = None

    def copy(self):
        copy = Game()
        copy.grid = self.grid.copy()
        copy.ball = self.ball
        copy.compute_stats()
        return copy

    def add(self, x, y, tile_id):
        self.grid[(x, y)] = self.mapping[tile_id]
        if tile_id == 4:
            self.ball = (x, y)

    def compute_stats(self):
        self.min_x = 0
        self.min_y = 0
        self.max_x = max(t[0] for t in self.grid.keys())
        self.max_y = max(t[1] for t in self.grid.keys())

    def display(self):
        for ry in range(self.max_y - self.min_y + 1):
            for rx in range(self.max_x - self.min_x + 1):
                x = self.min_x + rx
                y = self.min_y + ry
                print(self.grid[(x, y)], end='')
            print()
        print()

    def is_corner(self, pos):
        return pos == (self.min_x, self.min_y) or pos == (self.max_x, self.max_y)

    def is_top(self, pos):
        return pos[1] == 0

    def is_left(self, pos):
        return pos[0] == 0

    def is_right(self, pos):
        return pos[0] == self.max_x

    def start(self, direction):
        ball = self.ball
        while True:
            ball2 = ball[0] + direction[0], ball[1] + direction[1]
            if ball2 not in self.grid:
                return
            if self.grid[ball2] == '.' or self.grid[ball2] == ' ':
                self.grid[ball2] = 'x'
                ball = ball2
            elif self.grid[ball2] == '-':
                direction = direction[0], -1
            elif self.grid[ball2] == '#':
                if self.is_corner(ball2):
                    direction = (-direction[0], -direction[1])
                elif self.is_top(ball2):
                    direction = (direction[0], -direction[1])
                elif self.is_left(ball2) or self.is_right(ball2):
                    direction = (-direction[0], direction[1])
            else:
                ball = ball2

    def count_blocks(self):
        count = 0
        for y in range(self.max_y + 1):
            for x in range(self.max_x + 1):
                if self.grid[(x, y)] == '.':
                    count += 1

        return count


def main():
    m = Machine(ints(sys.stdin.readlines()[0]))
    m.inputs = [0]
    g = Game()
    while not m.halted:
        m.execute()
        m.execute()
        m.execute()
        x, y, tile_id = m.outputs[-3:]
        g.add(x, y, tile_id)

    g.compute_stats()
    g.display()

    copy = g.copy()
    copy.start((-1, -1))
    copy.display()
    print(copy.count_blocks())

    copy = g.copy()
    copy.start((1, -1))
    copy.display()
    print(copy.count_blocks())

    print(g.count_blocks())


if __name__ == '__main__':
    main()

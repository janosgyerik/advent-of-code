#!/usr/bin/env python3

import sys

from collections import defaultdict
from itertools import combinations


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
        self.backup = memory[:]
        self.reset()

    def reset(self):
        self.halted = False
        self.paused = False
        self.waiting_on_input = False
        self.ip = 0
        self.memory = defaultdict(lambda: 0, {i: v for i, v in enumerate(self.backup)})
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
    return [int(x) for x in line.split(',')]


shortcuts = {
    'e': 'east',
    'w': 'west',
    'n': 'north',
    's': 'south',
}


class AsciiMachine:
    def __init__(self, machine):
        self.machine = machine

    def execute(self, *commands):
        for command in commands:
            command = shortcuts[command] if command in shortcuts else command
            self.machine.inputs.extend(ord(c) for c in command + "\n")

        if self.machine.waiting_on_input:
            self.machine.execute()

        while not self.machine.waiting_on_input and not self.machine.halted:
            self.machine.execute()

        output = ''.join([chr(x) for x in self.machine.outputs])
        self.machine.outputs.clear()
        return output

    def inv(self):
        return self.execute('inv')

    def drop(self, item):
        return self.execute(f'drop {item}')

    def take(self, item):
        return self.execute(f'take {item}')

    def find_combination(self, command, items):
        for item in items:
            self.drop(item)

        for item in ('monolith', 'planetoid', 'fuel cell', 'astrolabe'):
            self.take(item)

        return
        for items_to_take in range(1, len(items) - 1):
            for combo in combinations(items, items_to_take):
                print(combo)
                for item in combo:
                    self.take(item)

                output = self.execute(command)
                if "you are ejected back" not in output:
                    return output

                for item in combo:
                    self.drop(item)

    def interact(self):
        print(self.execute())
        while True:
            command = input()
            if command == 'q':
                return

            print(self.execute(command))


def main():
    commands = [
        'e',
        'e',
        'e',
        'take shell',
        'w',
        's',
        'take monolith',
        'n',
        'w',
        'n',
        'w',
        'take bowl of rice',
        'e',
        'n',
        'take planetoid',
        'w',
        'take ornament',
        's',
        's',
        'take fuel cell',
        'n',
        'n',
        'e',
        'e',
        'take cake',
        's',
        'w',
        'n',
        'take astrolabe',
        'w',
        'n',
        'inv'
    ]

    items = [command[5:] for command in commands if command.startswith('take ')]

    with open('tmp/input.txt') as fh:
        m = AsciiMachine(Machine(ints(fh.read().rstrip())))
        m.execute(*commands)
        print(m.inv())
        print(m.find_combination('n', items))
        m.interact()


if __name__ == '__main__':
    main()

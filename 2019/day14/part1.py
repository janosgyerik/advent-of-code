#!/usr/bin/env python3

import sys

from collections import defaultdict, deque
from random import shuffle


class FuelComputer:
    def __init__(self):
        self.outputs = {}
        self.stock = defaultdict(lambda: 0)

    def add_output(self, o_name, o_count):
        self.outputs[o_name] = (o_count, [])

    def add_requirement(self, o_name, i_name, i_count):
        self.outputs[o_name][1].append((i_name, i_count))

    def compute(self, count, name):
        if name == 'ORE':
            return count

        unit_count, inputs = self.outputs[name]
        if self.stock[name]:
            if count < self.stock[name]:
                self.stock[name] -= count
                return 0
            count -= self.stock[name]
            self.stock[name] = 0

        # run a few times, and take the lowest value
        # yeah, lazy, but hey it's good enough
        shuffle(inputs)
        multiplier = self.compute_multiplier(count, unit_count)
        produced = sum(self.compute(multiplier * c, n) for n, c in inputs)
        if multiplier * unit_count > count:
            self.stock[name] += multiplier * unit_count - count

        return produced

    def compute_multiplier(self, count, unit_count):
        if count < unit_count:
            return 1

        if count % unit_count == 0:
            return count // unit_count

        return count // unit_count + 1


def parse_chemical(descriptor):
    count, name = descriptor.split(' ')
    return int(count), name


def parse_input(lines):
    fc = FuelComputer()
    for line in lines:
        inputs, output = line.rstrip().split(' => ')
        o_count, o_name = parse_chemical(output)
        fc.add_output(o_name, o_count)
        for input in inputs.split(', '):
            i_count, i_name = parse_chemical(input)
            fc.add_requirement(o_name, i_name, i_count)
    return fc


def main():
    fc = parse_input(sys.stdin.readlines())
    print(fc.compute(1, 'FUEL'))


if __name__ == '__main__':
    main()

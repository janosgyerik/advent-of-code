#!/usr/bin/env python

import sys


class Machine:
    def __init__(self, instructions):
        self.instructions = instructions
        self.mem = {}

    def execute(self):
        mask = {}
        for cmd, arg1, arg2 in self.instructions:
            if cmd == 'mask':
                mask = self.build_mask(arg1)
            else:
                address, value = arg1, arg2
                self.mem[address] = self.apply_mask(value, mask)

    def apply_mask(self, value, mask):
        for index, bit in mask.items():
            if bit == 1:
                value |= (1 << index)
            else:
                value &= ~(1 << index)

        return value

    def sumvalues(self):
        return sum(self.mem.values())

    def build_mask(self, maskspec):
        mask = {}
        len_maskspec = len(maskspec)
        for i in range(len_maskspec):
            m = maskspec[len_maskspec - i - 1]
            if m != 'X':
                mask[i] = int(m)

        return mask


def machine_from_lines(lines):
    instructions = []

    for line in lines:
        mspec, arg = line.split(' = ')
        if mspec == 'mask':
            instructions.append(('mask', arg, None))
        else:
            memstart = mspec.find('[') + 1
            memend = mspec.find(']')
            address = int(mspec[memstart:memend])
            value = int(arg)
            instructions.append(('asignment', address, value))

    return Machine(instructions)


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


def main():
    lines = read_lines(sys.argv[1])
    m = machine_from_lines(lines)
    m.execute()
    print(m.sumvalues())


if __name__ == '__main__':
    main()

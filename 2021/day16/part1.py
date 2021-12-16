#!/usr/bin/env python
import re
import sys
from collections import namedtuple, Counter, deque, defaultdict
from itertools import product
from heapq import heappush, heappop, heapify
from functools import lru_cache
from typing import List

import utils


def hex_digit_to_int(c):
    if '0' <= c <= '9':
        return int(c)

    if 'A' <= c <= 'F':
        return 10 + ord(c) - ord('A')

    raise ValueError


def to_word(num):
    bits = [0] * 4

    for index in range(4):
        bit = 1 << index
        value = num & bit
        if value:
            bits[3 - index] = 1

    return bits


def parse_bits(s):
    bits = []
    for c in s:
        bits.extend(to_word(hex_digit_to_int(c)))

    return bits


class Packet:
    def __init__(self, version, type_id, value=None, subpackets=None):
        self.version = version
        self.type_id = type_id
        self.value = value
        self.subpackets = subpackets if subpackets else []

    def print(self, indent=0):
        print(' ' * indent, self.version, self.type_id, self.value, len(self.subpackets))
        for p in self.subpackets:
            p.print(indent + 2)

    def version_sum(self):
        total = self.version
        for p in self.subpackets:
            total += p.version_sum()
        return total


def bits_to_int(bits):
    num = 0
    for b in bits:
        num *= 2
        num += b
    return num


class Parser:
    def __init__(self, bits):
        self.bits = bits
        self.length = len(bits)
        self.index = 0

    def parse_next(self):
        version = self.parse_int(3)
        type_id = self.parse_int(3)

        if type_id == 4:
            return self.parse_literal_value(version)
        else:
            return self.parse_operator(version, type_id)

    def parse_int(self, length):
        num = 0
        for _ in range(length):
            num *= 2
            num += self.bits[self.index]
            self.index += 1

        return num

    def parse_literal_value(self, version):
        value = 0
        while self.bits[self.index] != 0:
            self.index += 1
            value <<= 4
            value += self.parse_int(4)

        self.index += 1
        value <<= 4
        value += self.parse_int(4)

        return Packet(version, 4, value=value)

    def parse_operator(self, version, type_id):
        length_type_id = self.bits[self.index]
        self.index += 1

        subpackets = []

        if length_type_id == 0:
            length_of_subpackets = self.parse_int(15)
            limit = self.index + length_of_subpackets
            while self.index < limit:
                subpackets.append(self.parse_next())
        else:
            number_of_subpackets = self.parse_int(11)
            for _ in range(number_of_subpackets):
                subpackets.append(self.parse_next())

        return Packet(version, type_id, subpackets=subpackets)


def solve(lines):
    raw_bits = parse_bits(lines[0])
    packet = Parser(raw_bits).parse_next()
    return packet.version_sum()


def main():
    lines = utils.read_lines(sys.argv[1])
    print(solve(lines))


if __name__ == '__main__':
    main()

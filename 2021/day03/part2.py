#!/usr/bin/env python

import sys
from collections import namedtuple, Counter, deque, defaultdict
from itertools import product
from heapq import heappush, heappop, heapify
from functools import lru_cache


def ints(line):
    return [int(x) for x in line.split(' ')]


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


def solve(lines):
    count = 0
    nums = [int(v) for v in lines]
    wlen = 3
    window = sum(nums[0:wlen])
    index = wlen
    n = len(nums)
    prev = window
    while index < n:
        window += nums[index] - nums[index - wlen]
        if prev < window:
            count += 1
        prev = window
        index += 1

    return count


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines))


if __name__ == '__main__':
    main()
#!/usr/bin/env python

fn = 'sample.txt'
fn = 'input.txt'


def bits(line):
    return [int(c) for c in line]


def get_initial_lines():
    with open(fn) as fh:
        return [bits(line.rstrip()) for line in fh.readlines()]


def bit_counts(items, index):
    ones = 0
    zeros = 0

    for item in items:
        if item[index] == 0:
            zeros += 1
        else:
            ones += 1

    return [zeros, ones]


def most_frequent_bit(items, index):
    zeros, ones = bit_counts(items, index)
    return 1 if ones >= zeros else 0


def least_frequent_bit(items, index):
    zeros, ones = bit_counts(items, index)
    return 0 if zeros <= ones else 1


def filter_by_bit(items, index, bit):
    return [item for item in items if item[index] == bit]


def filter_by_bits(items, fun):
    for index in range(len(items[0])):
        bit = fun(items, index)
        items = filter_by_bit(items, index, bit)
        if len(items) == 1:
            return items[0]


def to_num(bits):
    num = 0
    for bit in bits:
        num <<= 1
        num += bit

    return num


def main():
    lines = get_initial_lines()
    oxygen = to_num(filter_by_bits(lines, most_frequent_bit))
    co2 = to_num(filter_by_bits(lines, least_frequent_bit))
    print(oxygen, co2, oxygen * co2)

main()

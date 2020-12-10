#!/usr/bin/env python

import sys
from collections import Counter


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


def part1(nums):
    seq = sorted(nums)
    seq = [0] + seq + [seq[-1] + 3]
    diffs = Counter(seq[i] - seq[i-1] for i in range(1, len(seq)))
    print(diffs[1], diffs[3], diffs[1] * diffs[3])


def main():
    lines = read_lines(sys.argv[1])
    nums = [int(x) for x in lines]
    part1(nums)


if __name__ == '__main__':
    main()

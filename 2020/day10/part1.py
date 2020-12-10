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
    return diffs


def part2(nums):
    '''
    (0), 1, 4, 5, 6, 7, 10, 11, 12, 15, 16, 19, (22)
    1    1  1  1  2  4   4   4   8   8   8   8    8
    ways = 0
    '''
    seq = sorted(nums)
    seq = [0] + seq + [seq[-1] + 3]
    ways = [0] * len(seq)
    ways[0] = 1

    for i, num in enumerate(seq):
        ways[i] += sum(ways[i - d] for d in range(1, 4) if i - d >= 0 and seq[i - d] + 3 >= num)

    return ways[-1]


def main():
    lines = read_lines(sys.argv[1])
    nums = [int(x) for x in lines]
    diffs = part1(nums)
    print(diffs[1] * diffs[3])
    print(part2(nums))


if __name__ == '__main__':
    main()

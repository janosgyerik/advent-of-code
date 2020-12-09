#!/usr/bin/env python

import sys
from collections import deque


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


def has_twosum(nums, target):
    seen = set()
    for num in nums:
        comp = target - num
        if comp in seen:
            return True
        seen.add(num)

    return False


def part1(preamble, nums):
    window = deque(nums[:preamble])
    for num in nums[preamble:]:
        if not has_twosum(window, num):
            return num
        window.popleft()
        window.append(num)


def main():
    preamble = int(sys.argv[1])
    lines = read_lines(sys.argv[2])
    nums = [int(x) for x in lines]
    print(part1(preamble, nums))


if __name__ == '__main__':
    main()

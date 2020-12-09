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


def find_range_to_sum(nums, target):
    sum_and_pos = {0: 0}
    cumul = 0
    for index, num in enumerate(nums):
        if (cumul - target) in sum_and_pos:
            return sum_and_pos[cumul - target], index

        cumul += num
        sum_and_pos[cumul] = index + 1


def part2(nums, target):
    start, end = find_range_to_sum(nums, target)
    part = nums[start:end]
    return min(part) + max(part)


def main():
    preamble = int(sys.argv[1])
    lines = read_lines(sys.argv[2])
    nums = [int(x) for x in lines]
    first_invalid = part1(preamble, nums)
    print(first_invalid)
    print(part2(nums, first_invalid))


if __name__ == '__main__':
    main()

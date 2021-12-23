#!/usr/bin/env python

import utils


def checksum(nums):
    nums.sort()

    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            x = nums[i]
            y = nums[j]
            if y % x == 0:
                return y // x


def solve(lines):
    total = 0
    for line in lines:
        nums = utils.parse_ints(line)
        total += checksum(nums)

    return total


if __name__ == '__main__':
    utils.solve(solve)

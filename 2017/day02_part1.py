#!/usr/bin/env python

import utils


def solve(lines):
    total = 0
    for line in lines:
        nums = utils.parse_ints(line)
        total += max(nums) - min(nums)

    return total


if __name__ == '__main__':
    utils.solve(solve)

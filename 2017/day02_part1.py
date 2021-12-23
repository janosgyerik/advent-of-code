#!/usr/bin/env python

import codebook


def solve(lines):
    total = 0
    for line in lines:
        nums = codebook.parse_ints(line)
        total += max(nums) - min(nums)

    return total


if __name__ == '__main__':
    codebook.solve(solve)

#!/usr/bin/env python3

import sys


def read_passes():
    return [line.strip() for line in sys.stdin.readlines()]


def to_seat_id(p):
    num = 0
    for i in range(7):
        c = p[i]
        num <<= 1
        if c == 'B':
            num |= 1

    for i in range(7, len(p)):
        c = p[i]
        num <<= 1
        if c == 'R':
            num |= 1

    return num


def compute_seat_ids(passes):
    return map(to_seat_id, passes)


def find_missing(nums):
    for i in range(1, len(nums)):
        if nums[i-1] + 1 < nums[i]:
            return nums[i] - 1


def main():
    passes = read_passes()
    seat_ids = list(compute_seat_ids(passes))
    print(max(seat_ids))
    print(find_missing(sorted(seat_ids)))


if __name__ == '__main__':
    main()

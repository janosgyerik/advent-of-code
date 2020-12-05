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


def seat_ids(bpasses):
    return map(to_seat_id, bpasses)


def main():
    passes = read_passes()
    print(max(seat_ids(passes)))


if __name__ == '__main__':
    main()

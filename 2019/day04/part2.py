#!/usr/bin/env python

import sys


def solve(start, end):
    count = 0
    for _ in gen(start, end):
        count += 1
    return count


def gen(start, end):
    current = start
    while current < end:
        if is_valid(current):
            yield current

        current += 1


def is_valid(code):
    next_digit = 10
    seen_doubled = False
    work = code
    repeat_count = 0
    while work > 0:
        current_digit = work % 10
        if current_digit > next_digit:
            return False
        if current_digit == next_digit:
            repeat_count += 1
        else:
            if repeat_count == 2:
                seen_doubled = True
            repeat_count = 1

        next_digit = current_digit
        work /= 10

    return seen_doubled or repeat_count == 2


def main():
    line = sys.stdin.read()
    start, end = [int(x) for x in line.rstrip().split('-')]
    print(solve(start, end))


if __name__ == '__main__':
    main()

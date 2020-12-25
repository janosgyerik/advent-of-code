#!/usr/bin/env python

import sys


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


def find_loop_size(subject, target):
    count = 0
    value = 1
    while value != target:
        value *= subject
        value %= 20201227
        count += 1

    return count


def transform(key, loop_size):
    value = 1
    for _ in range(loop_size):
        value *= key
        value %= 20201227
    return value


def main():
    lines = read_lines(sys.argv[1])
    keys = [int(line) for line in lines]
    loop_size = find_loop_size(7, keys[0])
    encryption_key = transform(keys[1], loop_size)
    print(encryption_key)


if __name__ == '__main__':
    main()

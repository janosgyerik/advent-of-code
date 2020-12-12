#!/usr/bin/env python

import sys
from collections import namedtuple


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


def moves_from_lines(lines):
    moves = []
    for line in lines:
        inst = line[0]
        step = int(line[1:])
        moves.append((inst, step))

    return moves


def apply_moves(moves, start):
    dirs = ((1, 0), (0, -1), (-1, 0), (0, 1))
    d = 0
    x, y = start
    for inst, step in moves:
        if inst == 'N':
            y += step
        elif inst == 'S':
            y -= step
        elif inst == 'E':
            x += step
        elif inst == 'W':
            x -= step
        elif inst == 'L':
            d = (d - (step // 90) + 4) % 4
        elif inst == 'R':
            d = (d + (step // 90)) % 4
        elif inst == 'F':
            x += dirs[d][0] * step
            y += dirs[d][1] * step

    return x, y


def main():
    lines = read_lines(sys.argv[1])
    moves = moves_from_lines(lines)
    start = 0, 0
    end_x, end_y = apply_moves(moves, start)
    print(abs(end_x) + abs(end_y))


if __name__ == '__main__':
    main()

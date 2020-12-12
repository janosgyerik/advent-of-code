#!/usr/bin/env python

import sys


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


def apply_moves(moves, wp):
    x, y = 0, 0
    wpx, wpy = wp
    for inst, step in moves:
        if inst == 'N':
            wpy += step
        elif inst == 'S':
            wpy -= step
        elif inst == 'E':
            wpx += step
        elif inst == 'W':
            wpx -= step
        elif inst == 'L':
            r = step // 90
            if r == 1:
                wpx, wpy = -wpy, wpx
            elif r == 2:
                wpx, wpy = -wpx, -wpy
            elif r == 3:
                wpx, wpy = wpy, -wpx
        elif inst == 'R':
            r = step // 90
            if r == 1:
                wpx, wpy = wpy, -wpx
            elif r == 2:
                wpx, wpy = -wpx, -wpy
            elif r == 3:
                wpx, wpy = -wpy, wpx
        elif inst == 'F':
            x += wpx * step
            y += wpy * step

    return x, y


def main():
    lines = read_lines(sys.argv[1])
    moves = moves_from_lines(lines)
    end_x, end_y = apply_moves(moves, (10, 1))
    print(abs(end_x) + abs(end_y))


if __name__ == '__main__':
    main()

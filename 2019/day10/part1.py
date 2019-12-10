#!/usr/bin/env python3

import sys


def find_asteroids(lines):
    for r in range(len(lines)):
        for c, v in enumerate(lines[r]):
            if v != '.':
                yield c, r


def angles(asteroids, a):
    return len(set(angle(a, b) for b in asteroids))


def sign(v):
    if v == 0:
        return 0
    if v > 0:
        return 1
    return -1


def direction(a, b):
    return sign(a[0] - b[0]), sign(a[1] - b[1])


def angle(a, b):
    d = direction(a, b)
    if a[0] == b[0]:
        return d, 'infx'
    if a[1] == b[1]:
        return d, 'infy'
    return d, (b[1] - a[1]) / (b[0] - a[0])


def main():
    lines = [x.rstrip() for x in sys.stdin.readlines()]
    asteroids = list(find_asteroids(lines))
    print(max(angles(asteroids, a) for a in asteroids) - 1)


if __name__ == '__main__':
    main()

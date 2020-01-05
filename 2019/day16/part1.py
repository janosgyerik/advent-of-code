#!/usr/bin/env python3

import sys

from collections import defaultdict, deque

PATTERN = [0, 1, 0, -1]


def apply_pattern(digits, rep):
    total = 0
    pcount = 1
    pattern = deque(PATTERN)
    for d in digits:
        if pcount >= rep:
            pattern.rotate(-1)
            pcount = 0
        pcount += 1
        total += pattern[0] * d
    return abs(total) % 10


def fft(digits):
    out = [0] * len(digits)
    for pos in range(len(digits)):
        rep = pos + 1
        out[pos] = apply_pattern(digits, rep)
    return out


def main():
    line = sys.stdin.read().rstrip()
    digits = [int(x) for x in line]
    for _ in range(100):
        digits = fft(digits)

    print(''.join(str(d) for d in digits[:8]))


if __name__ == '__main__':
    main()

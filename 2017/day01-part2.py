#!/usr/bin/env python

import codebook


def solve(lines):
    line = lines[0]
    total = 0
    n = len(line)
    step = n // 2
    for i in range(n):
        forward = (i + step) % n
        if line[i] == line[forward]:
            total += int(line[i])

    return total


if __name__ == '__main__':
    codebook.solve(solve)

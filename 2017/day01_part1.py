#!/usr/bin/env python

import utils


def solve(lines):
    line = lines[0]
    total = 0
    for i in range(-1, len(line) - 1):
        if line[i] == line[i+1]:
            total += int(line[i])

    return total


if __name__ == '__main__':
    utils.solve(solve)

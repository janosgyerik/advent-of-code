#!/usr/bin/env python

import sys
from functools import lru_cache

MOD = 20183
CFX = 16807
CFY = 48271


@lru_cache(maxsize=None)
def compute_erosion_level(depth, x, y, target):
    if (x, y) in ((0, 0), target):
        v = 0

    elif x == 0:
        v = y * CFY

    elif y == 0:
        v = x * CFX

    else:
        v = compute_erosion_level(depth, x-1, y, target) * compute_erosion_level(depth, x, y-1, target)

    return (v + depth) % MOD


def compute_risk_level(depth, target):
    total = 0
    tx, ty = target
    for x in range(tx + 1):
        for y in range(ty + 1):
            total += compute_erosion_level(depth, x, y, target) % 3

    return total


def main():
    depth = int(sys.argv[1])
    tx, ty = int(sys.argv[2]), int(sys.argv[3])
    risk_level = compute_risk_level(depth, (tx, ty))
    print(risk_level)

if __name__ == '__main__':
    main()

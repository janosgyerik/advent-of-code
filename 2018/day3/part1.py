#!/usr/bin/env python

import sys, re

overlaps = 0
covered = set()
counted = set()

dim = 1000

for line in sys.stdin.readlines():
    left, top, width, height = (int(x) for x in re.findall(r'(\d+),(\d+): (\d+)x(\d+)', line)[0])
    for x in range(width):
        for y in range(height):
            v = (left + x) * dim + top + y
            if v in covered:
                if v not in counted:
                    overlaps += 1
                counted.add(v)
            covered.add(v)

print(overlaps)

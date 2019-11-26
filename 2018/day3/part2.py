#!/usr/bin/env python

import sys, re

DIM = 1000


def pixels(rectangle):
    left, top, width, height = rectangle
    for x in range(width):
        for y in range(height):
            yield (left + x) * DIM + top + y


def has_overlap(rectangle):
    for pixel in pixels(rectangle):
        if pixel in counted:
            return True

    return False

covered = set()
counted = set()

lines = sys.stdin.readlines()
rectangles = [[int(x) for x in re.findall(r'(\d+),(\d+): (\d+)x(\d+)', line)[0]]
        for line in lines]

for rectangle in rectangles:
    for pixel in pixels(rectangle):
        if pixel in covered:
            counted.add(pixel)
        covered.add(pixel)

first_non_overlapping = next(i for i, rectangle in enumerate(rectangles)
        if not has_overlap(rectangle))

print(first_non_overlapping + 1)

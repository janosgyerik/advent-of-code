#!/usr/bin/env python
import re
import sys
from collections import namedtuple, Counter, deque, defaultdict
from itertools import product
from heapq import heappush, heappop, heapify
from functools import lru_cache


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


class Segment:
    def __init__(self, x1, y1, x2, y2):
        self._horizontal = y1 == y2
        self._vertical = x1 == x2
        if self._horizontal:
            if x2 < x1:
                x1, x2 = x2, x1

        elif self._vertical:
            if y2 < y1:
                y1, y2 = y2, y1

        else:
            if x2 < x1:
                x1, y1, x2, y2 = x2, y2, x1, y1

            dx = x2 - x1
            self._diagonal_down = dx == (y2 - y1)
            self._diagonal_up = dx == (y1 - y2)

        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    @property
    def is_horizontal(self):
        return self._horizontal

    @property
    def is_vertical(self):
        return self._vertical

    @property
    def is_diagonal_down(self):
        return self._diagonal_down

    @property
    def is_diagonal_up(self):
        return self._diagonal_up

    def __str__(self):
        return f"{self.x1},{self.y1} -> {self.x2},{self.y2} h={self.is_horizontal} v={self.is_vertical}"


def parse_input(lines):
    def to_pair(s):
        return [int(z) for z in s.split(',')]

    segments = []
    for line in lines:
        s1, s2 = line.split(' -> ')
        segments.append(Segment(*to_pair(s1), *to_pair(s2)))
    return segments


def compute_cover(segments):
    cover = defaultdict(int)
    for s in segments:
        if s.is_horizontal:
            for p in range(s.x1, s.x2 + 1):
                cover[(p, s.y1)] += 1
        elif s.is_vertical:
            for p in range(s.y1, s.y2 + 1):
                cover[(s.x1, p)] += 1
        elif s.is_diagonal_down:
            for d in range(s.x2 - s.x1 + 1):
                cover[(s.x1 + d, s.y1 + d)] += 1
        elif s.is_diagonal_up:
            for d in range(s.x2 - s.x1 + 1):
                cover[(s.x1 + d, s.y1 - d)] += 1

    return cover


def count_at_least_2(cover):
    return sum(1 for k, v in cover.items() if v > 1)


def solve(lines):
    segments = parse_input(lines)
    hv = [s for s in segments if s.is_horizontal or s.is_vertical or s.is_diagonal_down or s.is_diagonal_up]
    cover = compute_cover(hv)
    return count_at_least_2(cover)


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines))


if __name__ == '__main__':
    main()

#!/usr/bin/env python
import functools
import sys
from collections import namedtuple, Counter, deque, defaultdict
from dataclasses import dataclass
from functools import lru_cache
from heapq import heappush, heappop, heapify
from itertools import product


def ints(line):
    return [int(x) for x in line.split(' ')]


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


DIRS = {
    'L': (-1, 0),
    'R': (1, 0),
    'U': (0, 1),
    'D': (0, -1),
}


class Rope:
    def __init__(self):
        self.x = 0
        self.y = 0
        s = (0, 0)
        self.head = list(s)
        self.tail = list(s)
        self.visited = {s}

    def move(self, d, steps):
        x, y = self.head
        dx, dy = DIRS[d]

        for _ in range(steps):
            x += dx
            y += dy
            self.head[0] = x
            self.head[1] = y
            self.follow_head()

    def follow_head(self):
        dx = abs(self.head[0] - self.tail[0])
        dy = abs(self.head[1] - self.tail[1])
        if dx <= 1 and dy <= 1:
            return

        if dx == 2:
            if self.head[0] < self.tail[0]:
                self.tail[0] = self.head[0] + 1
            else:
                self.tail[0] = self.head[0] - 1

            self.tail[1] = self.head[1]

        elif dy == 2:
            if self.head[1] < self.tail[1]:
                self.tail[1] = self.head[1] + 1
            else:
                self.tail[1] = self.head[1] - 1

            self.tail[0] = self.head[0]

        elif self.head[0] + 2 == self.tail[0]:
            self.tail[0] = self.head[0] + 1
        elif self.head[0] - 2 == self.tail[0]:
            self.tail[0] = self.head[1] - 1
        elif self.head[1] + 2 == self.tail[1]:
            self.tail[1] = self.head[1] + 1
        elif self.head[1] - 2 == self.tail[1]:
            self.tail[1] = self.head[1] - 1
        else:
            raise ValueError(f'unexpected relative positions: head={self.head} tail={self.tail}')

        self.visited.add(tuple(self.tail))

    def count_visited(self):
        return len(self.visited)


def solve(lines):
    r = Rope()

    for line in lines:
        d, steps = line.split()
        steps = int(steps)
        r.move(d, steps)

    return r.count_visited()


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines))


if __name__ == '__main__':
    main()

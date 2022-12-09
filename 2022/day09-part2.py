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
        self.knots_count = 10
        self.knots = [list(s) for _ in range(self.knots_count)]
        self.head = self.knots[0]
        self.visited = {s}

    def move(self, d, steps):
        x, y = self.head
        dx, dy = DIRS[d]

        for _ in range(steps):
            x += dx
            y += dy
            self.head[0] = x
            self.head[1] = y
            for i in range(1, self.knots_count):
                self.follow(self.knots[i-1], self.knots[i])

            self.visited.add(tuple(self.knots[-1]))

    def follow(self, head, tail):
        dx = abs(head[0] - tail[0])
        dy = abs(head[1] - tail[1])

        if head[0] == tail[0]:
            if head[1] < tail[1]:
                tail[1] = head[1] + 1
            elif head[1] > tail[1]:
                tail[1] = head[1] - 1

        elif head[1] == tail[1]:
            if head[0] < tail[0]:
                tail[0] = head[0] + 1
            elif head[0] > tail[0]:
                tail[0] = head[0] - 1

        elif head[0] < tail[0] and head[1] < tail[1]:
            if dx > 1 or dy > 1:
                tail[0] -= 1
                tail[1] -= 1
        elif head[0] > tail[0] and head[1] > tail[1]:
            if dx > 1 or dy > 1:
                tail[0] += 1
                tail[1] += 1
        elif head[0] < tail[0] and head[1] > tail[1]:
            if dx > 1 or dy > 1:
                tail[0] -= 1
                tail[1] += 1
        elif head[0] > tail[0] and head[1] < tail[1]:
            if dx > 1 or dy > 1:
                tail[0] += 1
                tail[1] -= 1
        else:
            for knot in self.knots:
                print(knot)
            raise ValueError(f'unexpected relative positions: head={head} tail={tail}')

    def count_visited(self):
        for knot in self.knots:
            print(knot)
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

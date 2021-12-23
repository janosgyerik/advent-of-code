#!/usr/bin/env python

import utils
from collections import deque, defaultdict


class SpiralWalker:
    right = 1, 0
    up = 0, 1
    left = -1, 0
    down = 0, -1

    neighbors = [(1, 0), (-1, 0), (1, -1), (0, -1), (-1, -1), (1, 1), (0, 1), (-1, 1)]

    def __init__(self):
        self.x = 0
        self.y = 0
        self.dirs = deque([self.down, self.right, self.up, self.left])
        self.step_until = 0
        self.step = 0
        self.cumul = defaultdict(int)
        self.cumul[0, 0] = 1
        self.last = 0
        """
        1 right
        1 up
        2 left
        2 down
        3 right
        3 up
        4 left
        4 down
        5 right
        5 up
        """

    def advance(self):
        if self.step == self.step_until:
            self.step = 0
            self.dirs.rotate(-1)
            direction = self.dirs[0]
            if direction == self.right or direction == self.left:
                self.step_until += 1

        dx, dy = self.dirs[0]
        self.x += dx
        self.y += dy
        self.step += 1

        for dx, dy in self.neighbors:
            x2 = self.x + dx
            y2 = self.y + dy
            self.cumul[self.x, self.y] += self.cumul[x2, y2]

        self.last = self.cumul[self.x, self.y]


def solve(lines):
    n = int(lines[0])
    sw = SpiralWalker()
    for _ in range(1, n):
        sw.advance()
        if sw.last > n:
            return sw.last

    return abs(sw.x) + abs(sw.y)


if __name__ == '__main__':
    utils.solve(solve)

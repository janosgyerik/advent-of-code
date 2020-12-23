#!/usr/bin/env python

import sys
from collections import deque


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


class CrabCups:
    def __init__(self, cups):
        self.cups = deque(cups)

    def play(self):
        current = self.cups[0]

        self.cups.rotate(-1)
        removed = []
        for _ in range(3):
            removed.append(self.cups.popleft())

        destination = current - 1
        if destination == 0:
            destination = 9
        while destination in removed:
            destination -= 1
            if destination == 0:
                destination = 9

        start = self.cups.index(destination)
        for i in range(3):
            self.cups.insert(start + 1 + i, removed[i])

    def play_n(self, n):
        for _ in range(n):
            self.play()

    def score(self):
        cups = self.cups.copy()
        cups.rotate(-cups.index(1))
        cups.popleft()
        return ''.join(map(str, cups))


def main():
    lines = read_lines(sys.argv[1])
    crabcups = CrabCups([int(x) for x in lines[0]])
    crabcups.play_n(100)
    print(crabcups.score())


if __name__ == '__main__':
    main()

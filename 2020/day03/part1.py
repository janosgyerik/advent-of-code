#!/usr/bin/env python3

import sys
from functools import reduce

from itertools import permutations


class Mountain:
    def __init__(self, lines):
        self.lines = [line.strip() for line in lines]
        self._height = len(lines)
        self._width = len(self.lines[0])
        self.x = 0
        self.y = 0

    def height(self):
        return self._height

    def right(self, steps):
        self.x = (self.x + steps) % self._width

    def down(self, steps):
        self.y += steps

    def is_tree(self):
        if self.y >= self._height:
            return False
        return self.lines[self.y][self.x] == '#'

    def reset(self):
        self.x = 0
        self.y = 0


def count_trees(m, right, down):
    trees = 0
    m.reset()
    for _ in range(m.height() - 1):
        m.right(right)
        m.down(down)
        if m.is_tree():
            trees += 1

    return trees


def main():
    m = Mountain(sys.stdin.readlines())
    counts = (
        count_trees(m, 1, 1),
        count_trees(m, 3, 1),
        count_trees(m, 5, 1),
        count_trees(m, 7, 1),
        count_trees(m, 1, 2),
    )

    print(counts)
    print(reduce(lambda a, b: a * b, counts, 1))


if __name__ == '__main__':
    main()

#!/usr/bin/env python
import re
import sys
from collections import namedtuple, Counter, deque, defaultdict
from itertools import product
from heapq import heappush, heappop, heapify
from functools import lru_cache


hvd_neighbors = ((-1, 1), (-1, 0), (-1, -1), (0, 1), (0, -1), (1, 1), (1, 0), (1, -1))
hv_neighbors = ((0, 1), (1, 0), (0, -1), (-1, 0))


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


def letters_to_digits(letters):
    return [int(c) for c in letters]


def lines_of_digits_to_grid(lines):
    return [letters_to_digits(line) for line in lines]


class Graph:
    def __init__(self):
        self.adj = defaultdict(set)

    def connect(self, u, v):
        self.adj[u].add(v)
        self.adj[v].add(u)

    def print(self):
        print()


def parse_paper_and_instructions(lines):
    index = 0

    dots = []
    for line in lines:
        if not line:
            break

        x, y = [int(z) for z in line.split(',')]
        dots.append((x, y))

        index += 1

    instructions = []
    for line in lines[index+1:]:
        side, count = line.split('=')
        side = side[-1]
        count = int(count)
        instructions.append((side, count))

    return Paper(dots), instructions


class Paper:
    def __init__(self, dots):
        self.dots = sorted(dots)

    def fold_up(self, along):
        new_dots = set()
        n = max(y for x, y in self.dots)
        n += 1 - n % 2

        for dot in self.dots:
            x, y = dot
            if y < along:
                new_dots.add(dot)
            else:
                new_dots.add((x, n - y - 1))

        self.dots = sorted(list(new_dots))

    def fold_left(self, along):
        new_dots = set()
        n = max(x for x, y in self.dots)
        n += 1 - n % 2

        for dot in self.dots:
            x, y = dot
            if x < along:
                new_dots.add(dot)
            else:
                new_dots.add((n - x - 1, y))

        self.dots = sorted(list(new_dots))

    def count_dots(self):
        return len(self.dots)

    def print(self):
        dots = set(self.dots)

        max_x = max(x for x, y in self.dots)
        max_y = max(y for x, y in self.dots)

        for y in range(0, max_y + 1):
            for x in range(0, max_x + 1):
                if (x, y) in dots:
                    print('#', end='')
                else:
                    print(' ', end='')

            print()


def solve(lines):
    """
    dots are never on a folded line

    dots may overlap after a fold

    fold the bottom part onto up
    or fold the right part onto left
    """
    paper, instructions = parse_paper_and_instructions(lines)
    for side, count in instructions:
        if side == 'x':
            paper.fold_left(count)
        else:
            paper.fold_up(count)

    paper.print()


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines))


if __name__ == '__main__':
    main()

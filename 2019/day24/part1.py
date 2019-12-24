#!/usr/bin/env python3

import sys

from collections import defaultdict


class Life:
    def __init__(self):
        self.grid = 0

    def simulate(self):
        def cycle(v):
            if v >= 5:
                return 0
            if v < 0:
                return 4
            return v

        def is_alive(x, y):
            alive_neighbors = 0
            for dx, dy in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
                # x2, y2 = cycle(x + dx), cycle(y + dy)
                # if self.get(x2, y2):
                #     alive_neighbors += 1
                x2, y2 = x + dx, y + dy
                if 0 <= x2 < 5 and 0 <= y2 < 5:
                    if self.get(x2, y2):
                        alive_neighbors += 1

            if self.get(x, y):
                return alive_neighbors == 1

            return 1 <= alive_neighbors <= 2

        seen = {self.grid}

        while True:
            life2 = Life()
            for i in range(5):
                for j in range(5):
                    if is_alive(i, j):
                        life2.add(i, j)

            self.grid = life2.grid

            if self.grid in seen:
                break

            seen.add(self.grid)

    def biodiversity_rating(self):
        return self.grid

    def display(self):
        for row in range(5):
            for col in range(5):
                print(self.char_at(row, col), end='')
            print()
        print()

    def get(self, row, col):
        index = row*5 + col
        return self.grid & (1 << index) > 0

    def char_at(self, row, col):
        index = row*5 + col
        return '.#'[self.grid & (1 << index) > 0]

    def add(self, row, col):
        index = row*5 + col
        self.grid |= (1 << index)


def create_life(lines):
    life = Life()
    for row, line in enumerate(lines):
        for col, c in enumerate(line):
            if c == '#':
                life.add(row, col)
    return life


def main():
    lines = [line.rstrip() for line in sys.stdin.readlines()]
    life = create_life(lines)
    life.display()
    life.simulate()
    life.display()
    print(life.biodiversity_rating())


if __name__ == '__main__':
    main()

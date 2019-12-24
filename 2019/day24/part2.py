#!/usr/bin/env python3

import sys

from collections import defaultdict


class Life:
    def __init__(self):
        self.levels = defaultdict(lambda: 0)

    def display(self, level):
        for row in range(5):
            for col in range(5):
                print(self.char_at(row, col, level), end='')
            print()
        print()

    def display_all(self):
        for level in sorted(self.levels.keys()):
            print(f'level {level}:')
            self.display(level)
            print()

    def bit(self, row, col):
        return 1 << (row * 5 + col)

    def get(self, row, col, level):
        return self.levels[level] & self.bit(row, col) > 0

    def add(self, row, col, level):
        self.levels[level] |= self.bit(row, col)

    def char_at(self, row, col, level):
        return '.#'[self.get(row, col, level)]

    def simulate(self):
        def alive_in_row(row, inner_level):
            count = 0
            for col in range(5):
                if self.get(row, col, inner_level):
                    count += 1
            return count

        def alive_in_col(col, inner_level):
            count = 0
            for row in range(5):
                if self.get(row, col, inner_level):
                    count += 1
            return count

        def will_live(row, col, level):
            if col == 2 and row == 2:
                return False

            alive_neighbors = 0
            for dr, dc in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
                row2, col2 = row + dr, col + dc
                if col2 == 2 and row2 == 2:
                    if row == 1:
                        alive_neighbors += alive_in_row(0, level + 1)
                    elif row == 3:
                        alive_neighbors += alive_in_row(4, level + 1)
                    elif col == 1:
                        alive_neighbors += alive_in_col(0, level + 1)
                    elif col == 3:
                        alive_neighbors += alive_in_col(4, level + 1)
                elif 0 <= col2 < 5 and 0 <= row2 < 5:
                    alive_neighbors += self.get(row2, col2, level)
                elif col2 < 0:
                    alive_neighbors += self.get(2, 1, level - 1)
                elif col2 == 5:
                    alive_neighbors += self.get(2, 3, level - 1)
                elif row2 < 0:
                    alive_neighbors += self.get(1, 2, level - 1)
                elif row2 == 5:
                    alive_neighbors += self.get(3, 2, level - 1)

            if self.get(row, col, level):
                return alive_neighbors == 1

            return 1 <= alive_neighbors <= 2

        life2 = Life()
        levels = list(self.levels.keys())
        levels.append(min(level for level in levels if self.levels[level]) - 1)
        levels.append(max(level for level in levels if self.levels[level]) + 1)
        for level in levels:
            life2.levels[level] = 0
            for i in range(5):
                for j in range(5):
                    if will_live(i, j, level):
                        life2.add(i, j, level)

        self.levels = life2.levels.copy()

    def bugs(self):
        return sum(bin(n).count("1") for n in self.levels.values())


def create_life(lines):
    life = Life()
    for row, line in enumerate(lines):
        for col, c in enumerate(line):
            if c == '#':
                life.add(row, col, 0)
    return life


def main():
    lines = [line.rstrip() for line in sys.stdin.readlines()]
    life = create_life(lines)
    for _ in range(200):
        life.simulate()

    print(life.bugs())


if __name__ == '__main__':
    main()

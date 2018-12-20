#!/usr/bin/env python

import sys


class Computer:
    def __init__(self, serial):
        self.serial = serial

    def power(self, row, col):
        rack_id = row + 10
        return self.hundreds((rack_id * col + self.serial) * rack_id) - 5

    def hundreds(self, n):
        return (n // 100) % 10

    def print_grid(self, left, top, n):
        for y in range(top, top + n):
            for x in range(left, left + n):
                print('{:>3}'.format(self.power(x, y)), end=' ')
            print()

    def compute(self):
        highest, mx, my, mw = 0, 0, 0, 0
        for w in range(3, 30):
            v, x, y = self.compute_w(w)
            print(v, x, y, w)
            if highest < v:
                highest, mx, my, mw = v, x, y, w
        return highest, mx, my, mw

    def compute_w(self, w):
        left = 1
        top = 1
        n = 300
        grid = []
        for y in range(top, top + n):
            row = []
            for x in range(left, left + n):
                row.append(self.power(x, y))
            grid.append(row)

        highest = -5 * w * w
        mx = 0
        my = 0
        for y in range(n - w - 1):
            for x in range(n - w - 1):
                p = sum(sum(grid[y2][x:x+w]) for y2 in range(y, y+w))
                if highest < p:
                    highest, mx, my = p, x, y

        return highest, mx + 1, my + 1

if __name__ == '__main__':
    serial = int(sys.argv[1])
    c = Computer(serial)
    print(c.compute())

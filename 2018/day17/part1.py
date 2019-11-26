#!/usr/bin/env python

import sys, re
from collections import namedtuple

re_input_x = re.compile(r'x=(?P<x>\d+), y=(?P<y1>\d+)\.\.(?P<y2>\d+)')
re_input_y = re.compile(r'y=(?P<y>\d+), x=(?P<x1>\d+)\.\.(?P<x2>\d+)')

Segment = namedtuple('Segment', ['x1', 'x2', 'y1', 'y2'])

sys.setrecursionlimit(10000)


def ints(int_strings):
    return (int(v) for v in int_strings)


def parse_segment(s):
    '''
    >>> parse_segment('x=495, y=2..7')
    Segment(x1=495, x2=495, y1=2, y2=7)
    >>> parse_segment('y=7, x=495..501')
    Segment(x1=495, x2=501, y1=7, y2=7)
    '''
    m = re_input_x.match(s)
    if m:
        x, y1, y2 = ints(m.groups())
        return Segment(x, x, y1, y2)

    m = re_input_y.match(s)
    if m:
        y, x1, x2 = ints(m.groups())
        return Segment(x1, x2, y, y)

    raise ValueError('Could not parse as segment: ' + s)


class Landscape:
    def __init__(self, segments):
        self.min_y = min(segments, key=lambda s: s.y1).y1
        self.max_y = max(segments, key=lambda s: s.y2).y2
        self.min_x = min(segments, key=lambda s: s.x1).x1 - 1
        self.max_x = max(segments, key=lambda s: s.x2).x2 + 1
        self.grid = [['.'] * (self.max_x - self.min_x + 1) for _ in range(self.max_y - self.min_y + 1)]

        for segment in segments:
            for x in range(segment.x1, segment.x2 + 1):
                for y in range(segment.y1, segment.y2 + 1):
                    nx = x - self.min_x
                    ny = y - self.min_y
                    self.grid[ny][nx] = '#'

    def display(self):
        print(*(''.join(row) for row in self.grid), sep='\n')
        print()

    def count_water_reach(self):
        memo = {}

        def flow(x, y):
            def compute(x, y):
                if get_mark(x, y) != '.':
                    return False

                set_mark(x, y, '~')

                if y == self.max_y:
                    return True

                if flow(x, y + 1):
                    return True

                a = flow(x - 1, y)
                b = flow(x + 1, y)
                if a and not b:
                    i = 1
                    while get_mark(x + i, y) == '~':
                        memo[(x + i, y)] = True
                        i += 1
                return a or b

            if (x, y) in memo:
                return memo[(x, y)]

            result = compute(x, y)
            memo[(x, y)] = result
            return result

        def is_valid(x, y):
            return self.min_x <= x <= self.max_x and self.min_y <= y <= self.max_y

        def get_mark(x, y):
            if not is_valid(x, y):
                return None
            return self.grid[y - self.min_y][x - self.min_x]

        def set_mark(x, y, symbol):
            self.grid[y - self.min_y][x - self.min_x] = symbol

        flow(500, self.min_y)

        return sum(row.count('~') for row in self.grid)

if __name__ == '__main__':
    segments = [parse_segment(line) for line in sys.stdin.readlines()]
    landscape = Landscape(segments)
    count = landscape.count_water_reach()
    landscape.display()
    print(count)

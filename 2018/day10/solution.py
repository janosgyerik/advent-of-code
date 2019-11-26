#!/usr/bin/env python

import sys, re

pattern = re.compile(r'=<\s*(-?\d+), \s*(-?\d+)> velocity=<\s*(-?\d+), \s*(-?\d+)')


class Light:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def back(self):
        self.x -= self.vx
        self.y -= self.vy


def diff_x(lights):
    minx = min([o.x for o in lights])
    maxx = max([o.x for o in lights])
    return maxx - minx


def diff_y(lights):
    miny = min([o.y for o in lights])
    maxy = max([o.y for o in lights])
    return maxy - miny


def print_lights(lights):
    minx = min([o.x for o in lights])
    maxx = max([o.x for o in lights])
    miny = min([o.y for o in lights])
    maxy = max([o.y for o in lights])
    width = maxx - minx + 1
    height = maxy - miny + 1

    grid = [['.'] * width for _ in range(height)]
    for light in lights:
        grid[light.y - miny][light.x - minx] = '#'

    for row in grid:
        print(''.join(row))
    print()


if __name__ == '__main__':
    lights = []
    for line in sys.stdin.readlines():
        m = pattern.search(line)
        light = Light(*(int(x) for x in m.groups()))
        lights.append(light)

    prev_dx = diff_x(lights)
    prev_dy = diff_y(lights)
    for i in range(50000):
        dx = diff_x(lights)
        dy = diff_y(lights)
        if dx > prev_dx and dy > prev_dy:
            print(i - 1)
            for light in lights:
                light.back()
            print_lights(lights)
            break

        prev_dx = dx
        prev_dy = dy
        for light in lights:
            light.move()

#!/usr/bin/env python3

import sys


class SpaceImage:
    def __init__(self, pixels, width, height):
        self.pixels = pixels
        self.width = width
        self.height = height
        self.pagesize = width * height

    def layers(self):
        for start in range(0, len(self.pixels), self.pagesize):
            yield self.pixels[start:start + self.pagesize]


def main():
    si = SpaceImage(sys.stdin.read().rstrip(), 25, 6)
    fewest_0_layer = min(si.layers(), key=lambda x: x.count('0'))
    print(fewest_0_layer.count('1') * fewest_0_layer.count('2'))


if __name__ == '__main__':
    main()

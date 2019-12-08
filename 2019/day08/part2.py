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

    def rendered_pixels(self):
        rendered = [2] * self.pagesize
        for p in range(self.pagesize):
            for p2 in range(p, len(self.pixels), self.pagesize):
                if self.pixels[p2] != '2':
                    rendered[p] = self.pixels[p2]
                    break

        return ''.join(rendered)

    def display(self, pixels):
        for start in range(0, self.pagesize, self.width):
            print(pixels[start:start + self.width].replace('0', ' '))


def main():
    width, height = [int(x) for x in sys.argv[1:]]
    si = SpaceImage(sys.stdin.read().rstrip(), width, height)
    si.display(si.rendered_pixels())


if __name__ == '__main__':
    main()

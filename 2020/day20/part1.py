#!/usr/bin/env python

import sys
from collections import deque, defaultdict
from functools import reduce


def rev(num):
    r = 0
    for _ in range(10):
        r <<= 1
        r |= (num & 1)
        num >>= 1
    return r


class Tile:
    def __init__(self, tid, nums, edges):
        self.id = tid
        self.nums = nums
        self.edges = deque(edges)

    def can_match(self, other):
        for _ in range(4):
            for _ in range(4):
                if self.edges[0] == other.edges[0] or self.edges[0] == rev(other.edges[0]):
                    return True

                other.rotate(1)

            self.rotate(1)

        return False

    def rotate(self, count):
        self.edges.rotate(count)


def as_num(line):
    num = 0
    for c in line:
        num <<= 1
        if c == '#':
            num |= 1

    return num


def compute_edges(nums):
    edges = [nums[0]]

    right = 0
    for num in nums:
        right <<= 1
        right |= (num & 1)
    edges.append(right)

    bottom = 0
    work = nums[-1]
    for _ in range(10):
        bottom <<= 1
        bottom |= (work & 1)
        work >>= 1
    edges.append(bottom)

    left = 0
    for num in nums[::-1]:
        left <<= 1
        left |= (num & (1 << 9)) > 0
    edges.append(left)

    return edges


def parse_tile(tile_lines):
    tile_id = int(tile_lines[0][5:-1])
    nums = [as_num(line) for line in tile_lines[1:]]
    edges = compute_edges(nums)
    return Tile(tile_id, nums, edges)


def parse_tiles(lines):
    tiles = []
    tile_lines = []
    for line in lines:
        if not line:
            tiles.append(parse_tile(tile_lines))
            tile_lines.clear()
        else:
            tile_lines.append(line)

    return {tile.id: tile for tile in tiles}


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


class Graph:
    def __init__(self):
        self.adj = defaultdict(set)

    def connect(self, u, v):
        self.adj[u].add(v)
        self.adj[v].add(u)


def find_matches(tiles):
    g = Graph()
    for t1 in tiles.values():
        for t2 in tiles.values():
            if t1.id == t2.id:
                continue

            if t1.can_match(t2):
                g.connect(t1.id, t2.id)

    return g


def main():
    lines = read_lines(sys.argv[1])
    tiles = parse_tiles(lines)
    g = find_matches(tiles)

    corners = [tid for tid in tiles if len(g.adj[tid]) == 2]
    print(reduce(lambda a, b: a * b, corners, 1))


if __name__ == '__main__':
    main()

#!/usr/bin/env python

import sys
from collections import defaultdict, deque


monster = """
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """


def rev(num):
    r = 0
    for _ in range(10):
        r <<= 1
        r |= (num & 1)
        num >>= 1
    return r


def rot90(matrix):
    return [[row[i] for row in matrix][::-1] for i in range(len(matrix))]


class Image:
    def __init__(self, matrix):
        self.matrix = matrix

        self.mpos = []
        dr = 0
        for line in monster.split('\n')[1:]:
            for dc, c in enumerate(line):
                if c == '#':
                    self.mpos.append((dr, dc))
            dr += 1

    def count_monsters(self):
        count = 0
        for r in range(len(self.matrix) - 2):
            for c in range(len(self.matrix[0]) - 19):
                for dr, dc in self.mpos:
                    r2 = r + dr
                    c2 = c + dc
                    if self.matrix[r2][c2] != '#':
                        break
                else:
                    count += 1

        return count

    def count_pixels(self):
        return sum(row.count('#') for row in self.matrix)

    def count_not_monster_pixels(self, count):
        return self.count_pixels() - count * monster.count('#')

    def rotate(self):
        self.matrix = rot90(self.matrix)

    def hflip(self):
        self.matrix = self.matrix[::-1]


class Tile:
    def __init__(self, tid, nums, edges, lines):
        self.id = tid
        self.nums = nums
        self.edges = deque(edges)
        self.keys = set(edges + [rev(edge) for edge in edges])
        self.horiz = {edges[1], edges[3]}
        self.horiz.update({rev(edge) for edge in self.horiz})
        self.vert = {edges[0], edges[2]}
        self.vert.update({rev(edge) for edge in self.vert})
        self.matrix = [[c for c in line] for line in lines]

    def print(self):
        print(f"Tile {self.id}")
        for row in self.matrix:
            print(''.join(row))
        print()

    def can_match(self, other):
        return self.keys.intersection(other.keys)

    def can_match_horiz(self, other):
        return self.horiz.intersection(other.horiz)

    def can_match_vert(self, other):
        return self.vert.intersection(other.vert)

    def fit_at_right(self, right):
        intersection = self.can_match_horiz(right)
        if self.edges[1] not in intersection or rev(self.edges[1]) not in intersection:
            self.hflip()

        if right.edges[3] not in intersection or rev(right.edges[3]) not in intersection:
            right.hflip()

        if self.edges[1] != right.edges[3]:
            right.vflip()

        if not right.is_right_of(self):
            self.print()
            right.print()
        assert right.is_right_of(self)

    def fit_at_bottom(self, bottom):
        intersection = self.can_match_vert(bottom)
        if self.edges[2] not in intersection or rev(self.edges[2]) not in intersection:
            self.vflip()

        if bottom.edges[0] not in intersection or rev(bottom.edges[0]) not in intersection:
            bottom.vflip()

        if not bottom.is_bottom_of(self):
            bottom.hflip()

        if not bottom.is_bottom_of(self):
            self.print()
            bottom.print()
        assert bottom.is_bottom_of(self)

    def vflip(self):
        self.matrix = self.matrix[::-1]
        self.edges[0], self.edges[2] = self.edges[2], self.edges[0]
        self.edges[1] = rev(self.edges[1])
        self.edges[3] = rev(self.edges[3])

    def hflip(self):
        self.matrix = [row[::-1] for row in self.matrix]
        self.edges[1], self.edges[3] = self.edges[3], self.edges[1]
        self.edges[0] = rev(self.edges[0])
        self.edges[2] = rev(self.edges[2])

    def rotate(self):
        self.matrix = rot90(self.matrix)
        self.rebuild_edges()
        self.horiz = {self.edges[1], self.edges[3]}
        self.horiz.update({rev(edge) for edge in self.horiz})
        self.vert = {self.edges[0], self.edges[2]}
        self.vert.update({rev(edge) for edge in self.vert})

    def rebuild_edges(self):
        self.edges[0] = self.row_as_num(0)
        self.edges[1] = self.col_as_num(-1)
        self.edges[2] = self.row_as_num(-1)
        self.edges[3] = self.col_as_num(0)

    def row_as_num(self, r):
        num = 0
        for c in self.matrix[r]:
            num <<= 1
            num |= c == '#'
        return num

    def col_as_num(self, c):
        num = 0
        for row in self.matrix:
            num <<= 1
            num |= row[c] == '#'
        return num

    @property
    def top(self):
        return self.edges[0]

    @property
    def right(self):
        return self.edges[1]

    @property
    def bottom(self):
        return self.edges[2]

    @property
    def left(self):
        return self.edges[3]

    def is_right_of(self, base):
        return self.left == base.right

    def is_bottom_of(self, base):
        return self.top == base.bottom


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

    edges.append(nums[-1])

    left = 0
    for num in nums:
        left <<= 1
        left |= (num & (1 << 9)) > 0
    edges.append(left)

    return edges


def parse_tile(tile_lines):
    tile_id = int(tile_lines[0][5:-1])
    lines = tile_lines[1:]
    nums = [as_num(line) for line in lines]
    edges = compute_edges(nums)
    return Tile(tile_id, nums, edges, lines)


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


def find_any_corner(tiles, g):
    for k, v in g.adj.items():
        if len(v) == 2:
            return tiles[k]


def make_top_left(corner, tiles, g):
    v1, v2 = [tiles[v] for v in g.adj[corner.id]]
    if corner.can_match_horiz(v1) == corner.can_match_horiz(v2):
        v1.rotate()

    if corner.can_match_horiz(v1):
        right = v1
        bottom = v2
    else:
        right = v2
        bottom = v1

    corner.fit_at_right(right)
    assert right.is_right_of(corner)

    if not corner.can_match_vert(bottom):
        bottom.rotate()
    assert corner.can_match_vert(bottom)
    corner.fit_at_bottom(bottom)

    assert bottom.is_bottom_of(corner)

    return corner


def build_image(tiles, g):
    corner = find_any_corner(tiles, g)
    top_left = make_top_left(corner, tiles, g)

    q = deque([top_left])
    coords = {top_left.id: (0, 0)}
    while q:
        base = q.popleft()
        r, c = coords[base.id]

        right = None
        bottom = None

        for v in g.adj[base.id]:
            if v in coords:
                continue

            other = tiles[v]

            for _ in range(4):
                if base.can_match_horiz(other):
                    right = other
                    break
                other.rotate()
            else:
                for _ in range(4):
                    if base.can_match_vert(other):
                        bottom = other
                        break
                    other.rotate()
                else:
                    raise ValueError('could not match as either right or bottom')

            q.append(other)

        if right is not None:
            base.fit_at_right(right)
            coords[right.id] = r, c + 1

        if bottom is not None:
            base.fit_at_bottom(bottom)
            coords[bottom.id] = r + 1, c

    max_r = max(r for r, c in coords.values())
    max_c = max(c for r, c in coords.values())

    rcoords = {pos: tid for tid, pos in coords.items()}

    grid = []
    for r in range(max_r + 1):
        for r2 in range(1, 9):
            row = []
            for c in range(max_c + 1):
                tile = tiles[rcoords[r, c]]
                row.extend(tile.matrix[r2][1:9])
            grid.append(row)

    return Image(grid)


def main():
    lines = read_lines(sys.argv[1])
    tiles = parse_tiles(lines)
    g = find_matches(tiles)

    image = build_image(tiles, g)
    for i in range(8):
        count = image.count_monsters()
        if count > 0:
            print(image.count_not_monster_pixels(count))
            break

        image.rotate()
        if i == 3:
            image.hflip()


if __name__ == '__main__':
    main()

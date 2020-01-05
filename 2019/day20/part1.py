#!/usr/bin/env python3

import sys
from collections import defaultdict


class Maze:
    def __init__(self):
        self.neighbors = defaultdict(set)
        self.portal_name_to_pos = {}
        self.portal_pos_to_name = {}

    def add_portal(self, pos, name):
        self.portal_pos_to_name[pos] = name
        if name in self.portal_name_to_pos:
            self.connect(self.portal_name_to_pos[name], pos)
        else:
            self.portal_name_to_pos[name] = pos

    def portal(self, name):
        return self.portal_name_to_pos[name]

    def connect(self, pos, other):
        self.neighbors[pos].add(other)
        self.neighbors[other].add(pos)

    def shortest_path(self, start, end):
        q = [(start, 0)]
        visited = set()
        while q:
            pos, d = q.pop(0)
            if pos == end:
                return d

            visited.add(pos)

            for pos2 in self.neighbors[pos]:
                if pos2 not in visited:
                    q.append((pos2, d+1))


def create_maze(lines):
    maze = Maze()

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for y in range(2, len(lines) - 2):
        for x in range(2, len(lines[0]) - 2):
            if lines[y][x] == '.':
                pos = x, y
                for dx, dy in directions:
                    pos2 = x2, y2 = x+dx, y+dy
                    c = lines[y2][x2]
                    if c.isupper() or c == '.':
                        maze.connect(pos, pos2)
                        if c.isupper():
                            if lines[y2][x2+1].isupper():
                                name = c + lines[y2][x2+1]
                            elif lines[y2][x2-1].isupper():
                                name = lines[y2][x2-1] + c
                            elif lines[y2+1][x2].isupper():
                                name = c + lines[y2+1][x2]
                            elif lines[y2-1][x2].isupper():
                                name = lines[y2-1][x2] + c
                            else:
                                raise ValueError('expected an uppercase neighbor')

                            maze.add_portal(pos, name)

    return maze


def main():
    lines = [line for line in sys.stdin.readlines()]
    maze = create_maze(lines)
    print(maze.shortest_path(maze.portal('AA'), maze.portal('ZZ')))


if __name__ == '__main__':
    main()

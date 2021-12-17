#!/usr/bin/env python3

import sys
from collections import defaultdict


class Maze:
    def __init__(self):
        self.neighbors = defaultdict(set)
        self.portal_name_to_pos = {}
        self.portal_pos_to_name = {}
        self.max_x = 0
        self.max_y = 0

    def add_portal(self, pos, name):
        self.portal_pos_to_name[pos] = name
        if name in self.portal_name_to_pos:
            self.connect(self.portal_name_to_pos[name], pos)
        else:
            self.portal_name_to_pos[name] = pos

        self.max_x = max(self.max_x, pos[0])
        self.max_y = max(self.max_y, pos[1])

    def get_level_offset(self, pos):
        if pos[0] <= 3 or pos[1] <= 3 or pos[0] >= self.max_x - 3 or pos[1] >= self.max_y - 3:
            return 1
        return -1

    def portal(self, name):
        return self.portal_name_to_pos[name]

    def connect(self, pos, other):
        self.neighbors[pos].add(other)
        self.neighbors[other].add(pos)

    def shortest_path(self, start, end):
        def is_outer(pos):
            return pos[0] <= 3 or pos[1] <= 3 or pos[0] >= self.max_x - 3 or pos[1] >= self.max_y - 3

        def is_wall(pos, level):
            return (level and self.portal_pos_to_name.get(pos) in ('AA', 'ZZ')
                    or level == 0 and pos in self.portal_pos_to_name and is_outer(pos))

        def compute_level(pos, level):
            if pos not in self.portal_pos_to_name:
                return level

            if self.portal_pos_to_name[pos] in ('AA', 'ZZ'):
                return level

            return level + self.get_level_offset(pos)

        path = {(start, 0): None}

        def print_path():
            p = (end, 0)
            steps = [p]
            while True:
                p = path[p]
                if p is None:
                    break
                steps.append(p)
            for p in reversed(steps):
                print(p[0][1], p[0][0], p[1])

        q = [(start, 0, 0)]
        visited = {(start, 0)}
        # for pos, name in sorted(self.portal_pos_to_name.items()):
        #     print(f"{pos}: {name}")
        while q:
            pos, level, d = q.pop(0)
            # print(pos, level, d)
            print(d)
            if pos == end:
                print_path()
                return d

            for pos2 in self.neighbors[pos]:
                if is_wall(pos2, level):
                    continue

                level2 = compute_level(pos, level)
                if (pos2, level2) not in visited:
                    visited.add((pos2, level2))
                    q.append((pos2, level2, d + 1))
                    path[pos2, level2] = (pos, level)


def create_maze(lines):
    maze = Maze()

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for y in range(2, len(lines) - 2):
        for x in range(2, len(lines[0]) - 2):
            if lines[y][x] == '.':
                pos = x, y
                for dx, dy in directions:
                    pos2 = x2, y2 = x + dx, y + dy
                    c = lines[y2][x2]
                    if c.isupper() or c == '.':
                        maze.connect(pos, pos2)
                        if c.isupper():
                            if lines[y2][x2 + 1].isupper():
                                name = c + lines[y2][x2 + 1]
                            elif lines[y2][x2 - 1].isupper():
                                name = lines[y2][x2 - 1] + c
                            elif lines[y2 + 1][x2].isupper():
                                name = c + lines[y2 + 1][x2]
                            elif lines[y2 - 1][x2].isupper():
                                name = lines[y2 - 1][x2] + c
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

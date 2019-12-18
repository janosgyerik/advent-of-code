#!/usr/bin/env python3

import sys

from collections import defaultdict


class Maze:
    def __init__(self):
        self.grid = {}
        self.name_to_pos = {}
        self.neighbors = defaultdict(set)
        self.keys_count = 0

    def add(self, x, y, name):
        pos = (x, y)
        self.grid[pos] = name
        self.name_to_pos[name] = pos

    def connect(self, pos, pos2):
        self.neighbors[pos].add(pos2)
        self.neighbors[pos2].add(pos)

    def pos(self, name):
        return self.name_to_pos[name]

    def min_steps_to_collect_all_keys(self):
        def add_key(store, key):
            if not ('a' <= key <= 'z'):
                raise ValueError(f'key must be a lowercase letter, got "{key}"')

            return store | (1 << (ord(key) - ord('a')))

        def can_open(store, lock):
            if not ('A' <= lock <= 'Z'):
                raise ValueError(f'lock must be an uppercase letter, got "{lock}')

            bit = 1 << (ord(lock) - ord('A'))
            return store & bit > 0

        def is_key(c):
            return 'a' <= c <= 'z'

        def is_lock(c):
            return 'A' <= c <= 'Z'

        all_keys = 2 ** len([name for name in self.name_to_pos.keys() if name.islower()]) - 1
        pos = self.pos('@')
        seen = {(pos, 0)}
        q = [(pos, 0, 0)]
        while q:
            pos, keys, d = q.pop(0)

            for pos2 in self.neighbors[pos]:
                if (pos2, keys) in seen:
                    continue

                seen.add((pos2, keys))
                name2 = self.grid[pos2]
                if is_lock(name2) and not can_open(keys, name2):
                    continue

                if is_key(name2):
                    keys2 = add_key(keys, name2)
                    if keys2 == all_keys:
                        return d + 1

                    q.append((pos2, keys2, d + 1))

                else:
                    q.append((pos2, keys, d + 1))


def create_maze(lines):
    maze = Maze()
    for y, line in enumerate(lines):
        for x, c in enumerate(line.rstrip()):
            if c != '#':
                maze.add(x, y, c)

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for pos in maze.grid:
        x, y = pos
        for dx, dy in directions:
            pos2 = x + dx, y + dy
            if pos2 in maze.grid:
                maze.connect(pos, pos2)

    return maze


def main():
    maze = create_maze(sys.stdin.readlines())
    print(maze.min_steps_to_collect_all_keys())


if __name__ == '__main__':
    main()

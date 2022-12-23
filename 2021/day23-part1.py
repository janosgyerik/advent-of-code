#!/usr/bin/env python
import itertools
import sys

import math
from numbers import Number
from typing import Callable, Any

from utils import graphs
import re
from collections import namedtuple, Counter, deque, defaultdict
from itertools import product
from heapq import heappush, heappop, heapify
from functools import lru_cache


def parse_state(lines):
    rooms = [
        [to_num(lines[3][3]), to_num(lines[2][3])],
        [to_num(lines[3][5]), to_num(lines[2][5])],
        [to_num(lines[3][7]), to_num(lines[2][7])],
        [to_num(lines[3][9]), to_num(lines[2][9])],
    ]
    return State(rooms)


def to_letter(num):
    assert 0 <= num <= 4
    if num == 0:
        return '.'
    return chr(ord('A') + num - 1)


def to_num(letter):
    assert 'A' <= letter <= 'D'
    return ord(letter) - ord('A') + 1


def copy_2d(grid):
    return [row[:] for row in grid]


class State:
    def __init__(self, rooms):
        self.hallway = [0] * 11
        self.rooms = rooms

    def print(self):
        print('#' * 13)

        hallway = [c for c in '#' + ('.' * 11) + '#']
        for i, num in enumerate(self.hallway):
            hallway[1 + i] = to_letter(num)
        print(''.join(hallway))

        def room(r, pos):
            if pos >= len(self.rooms[r]):
                return '.'
            return to_letter(self.rooms[r][pos])

        print('###' + '#'.join([room(0, 1), room(1, 1), room(2, 1), room(3, 1)]) + '###')
        print('  #' + '#'.join([room(0, 0), room(1, 0), room(2, 0), room(3, 0)]) + '#')
        print('  ' + '#' * 9)
        print()

    def __hash__(self):
        h = 0
        for x in self.hallway:
            h *= 5
            h += x

        for room in self.rooms:
            if len(room) == 0:
                h *= 5 * 5
            elif len(room) == 1:
                h *= 5 * 5
                h += room[0]
            else:
                for x in room:
                    h *= 5
                    h += x

        return h

    def __eq__(self, other):
        return (self.hallway == other.hallway
                and self.rooms == other.rooms)

    def adj(self):
        ans = []
        for i, room in enumerate(self.rooms):
            ans.extend(self.moves_from_room(i))

        for i in range(len(self.hallway)):
            ans.extend(self.moves_from_hallway(i))

        return ans

    def moves_from_room(self, room_id):
        room = self.rooms[room_id]
        if len(room) == 0 or all(j == room_id + 1 for j in room):
            return []

        step_cost = self.step_cost(room[-1])

        if len(room) == 1:
            base_cost = step_cost * 2
        else:
            base_cost = step_cost

        hallway_pos = self.hallway_pos(room_id)
        assert self.hallway[hallway_pos] == 0

        ans = []

        # moves to left of hallway
        for j in range(hallway_pos - 1, -1, -1):
            # do not stop over rooms
            if j > 0 and j % 2 == 0:
                continue

            if self.hallway[j] != 0:
                break

            steps = hallway_pos - j
            cost = base_cost + steps * step_cost
            ans.append((self.after_move_to_hallway(room_id, j), cost))

        # moves to right of hallway
        for j in range(hallway_pos + 1, len(self.hallway)):
            # do not stop over rooms
            if j < len(self.hallway) - 1 and j % 2 == 0:
                continue

            if self.hallway[j] != 0:
                break

            steps = j - hallway_pos
            cost = base_cost + steps * step_cost
            ans.append((self.after_move_to_hallway(room_id, j), cost))

        return ans

    def moves_from_hallway(self, hallway_pos):
        if self.hallway[hallway_pos] == 0:
            return []

        ans = []

        step_cost = self.step_cost(self.hallway[hallway_pos])
        for room_id, room in enumerate(self.rooms):
            steps_to_room = self.steps_to_room(hallway_pos, room_id)
            if steps_to_room:
                cost = step_cost * steps_to_room
                ans.append((self.after_move_to_room(hallway_pos, room_id), cost))

        return ans

    def step_cost(self, x):
        return 10 ** (x - 1)

    def hallway_pos(self, room_id):
        return 2 + room_id * 2

    def steps_to_room(self, hallway_pos, room_id):
        if len(self.rooms[room_id]) == 2:
            return 0

        if self.hallway[hallway_pos] != room_id + 1:
            return 0

        room_hallway_pos = self.hallway_pos(room_id)
        assert hallway_pos != room_hallway_pos

        step = 1 if hallway_pos < room_hallway_pos else -1
        for h in range(hallway_pos + step, room_hallway_pos, step):
            if self.hallway[h] != 0:
                return 0

        return abs(room_hallway_pos - hallway_pos) + 2 - len(self.rooms[room_id])

    def copy(self):
        rooms = copy_2d(self.rooms)
        copy = State(rooms)
        copy.hallway = self.hallway[:]
        return copy

    def after_move_to_hallway(self, room_id, hallway_pos):
        assert self.hallway[hallway_pos] == 0

        copy = self.copy()
        num = copy.rooms[room_id].pop()
        copy.hallway[hallway_pos] = num
        return copy

    def after_move_to_room(self, hallway_pos, room_id):
        assert self.hallway[hallway_pos] != 0
        assert len(self.rooms[room_id]) < 2

        copy = self.copy()
        copy.rooms[room_id].append(self.hallway[hallway_pos])
        copy.hallway[hallway_pos] = 0
        return copy


def create_graph(start):
    g = graphs.Graph()
    weights = {}

    ids = {}

    def get_or_create_id(x):
        if x in ids:
            return ids[x]

        ids[x] = len(ids)

    def dfs(u):
        if u in seen:
            return

        seen.add(u)
        uid = get_or_create_id(u)
        for v, weight in u.adj():
            vid = get_or_create_id(v)
            # weights[uid, vid] = weight
            # g.connect(uid, vid)
            weights[u, v] = weight
            g.connect(u, v)
            dfs(v)

    seen = set()
    dfs(start)
    return g, weights, ids


def solve(lines):
    state = parse_state(lines)
    state.print()

    g, weights, ids = create_graph(state)

    target = State([[1, 1], [2, 2], [3, 3], [4, 4]])
    # return graphs.dijkstra(g, state, target, lambda a, b: weights[a, b])
    return graphs.dijkstra(g, state, target, lambda a, b: weights.get((a, b), float('inf')))
    # return graphs.dijkstra(g, ids[state], ids[target], lambda a, b: weights.get((a, b), float('inf')))
    # return graphs.dijkstra(g, ids[state], ids[target], lambda a, b: weights[a, b])


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines))


if __name__ == '__main__':
    main()

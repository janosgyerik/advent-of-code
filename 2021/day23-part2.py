#!/usr/bin/env python
import math
from numbers import Number
from typing import Callable, Any

import utils
import re
from collections import namedtuple, Counter, deque, defaultdict
from itertools import product
from heapq import heappush, heappop, heapify
from functools import lru_cache
import utils


ROOM_CAPACITY = 4


def parse_state(lines):
    rooms = [
        [to_num(lines[3][3]), to_num(lines[2][3])],
        [to_num(lines[3][5]), to_num(lines[2][5])],
        [to_num(lines[3][7]), to_num(lines[2][7])],
        [to_num(lines[3][9]), to_num(lines[2][9])],
    ]

    if ROOM_CAPACITY > 2:
        rooms[0].insert(1, 4)
        rooms[0].insert(1, 4)
        rooms[1].insert(1, 3)
        rooms[1].insert(1, 2)
        rooms[2].insert(1, 2)
        rooms[2].insert(1, 1)
        rooms[3].insert(1, 1)
        rooms[3].insert(1, 3)

    return State(rooms)


def to_letter(num):
    assert 0 <= num <= 4
    if num == 0:
        return '.'
    return chr(ord('A') + num - 1)


def to_num(letter):
    assert 'A' <= letter <= 'D'
    return ord(letter) - ord('A') + 1


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

        print('###' + '#'.join([room(x, ROOM_CAPACITY - 1) for x in range(4)]) + '###')
        for pos in range(ROOM_CAPACITY - 2, -1, -1):
            print('  #' + '#'.join([room(x, pos) for x in range(4)]) + '#')
        print('  ' + '#' * 9)
        print()

    def __hash__(self):
        state = self.hallway[:]
        for room in self.rooms:
            for _ in range(ROOM_CAPACITY - len(room)):
                state.append(0)
            state += room

        h = 0
        for x in state:
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
        base_cost = step_cost * (ROOM_CAPACITY - len(room) + 1)

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
        if len(self.rooms[room_id]) == ROOM_CAPACITY:
            return 0

        if self.hallway[hallway_pos] != room_id + 1:
            return 0

        if not all(v == room_id + 1 for v in self.rooms[room_id]):
            return 0

        room_hallway_pos = self.hallway_pos(room_id)
        assert hallway_pos != room_hallway_pos

        step = 1 if hallway_pos < room_hallway_pos else -1
        for h in range(hallway_pos + step, room_hallway_pos, step):
            if self.hallway[h] != 0:
                return 0

        return abs(room_hallway_pos - hallway_pos) + ROOM_CAPACITY - len(self.rooms[room_id])

    def copy(self):
        rooms = utils.copy_2d(self.rooms)
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
        assert self.hallway[hallway_pos] == room_id + 1
        assert all(v == room_id + 1 for v in self.rooms[room_id])
        assert len(self.rooms[room_id]) < ROOM_CAPACITY

        copy = self.copy()
        copy.rooms[room_id].append(self.hallway[hallway_pos])
        copy.hallway[hallway_pos] = 0
        return copy


class Memo:
    def __init__(self):
        self.memo = {}

    def adj(self, state):
        if state not in self.memo:
            adj = state.adj()
            self.memo[state] = adj

        return self.memo[state]


def dijkstra(start, end):
    dist = {start: 0}

    pq = utils.PriorityQueue()
    pq.add_or_update(start, 0)

    done = set()

    graph = Memo()

    while pq:
        u = pq.pop()
        if u == end:
            break

        done.add(u)

        for v, weight in graph.adj(u):
            if v in done:
                continue

            alt = dist[u] + weight
            if alt < dist.get(v, float('inf')):
                dist[v] = alt
                pq.add_or_update(v, alt)

    return dist[end]


def solve(lines):
    state = parse_state(lines)
    state.print()

    target = State([[x + 1] * ROOM_CAPACITY for x in range(4)])
    return dijkstra(state, target)


if __name__ == '__main__':
    utils.solve(solve)

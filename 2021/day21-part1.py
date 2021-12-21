#!/usr/bin/env python
import math

import utils
import re
from collections import namedtuple, Counter, deque, defaultdict
from itertools import product
from heapq import heappush, heappop, heapify
from functools import lru_cache
import utils


def parse_input(lines):
    return int(lines[0][-1]), int(lines[1][-1])


def ddie(n):
    while True:
        for i in range(1, n + 1):
            yield i


class Player:
    def __init__(self, pos, max_pos, die, rolls, target_score):
        self.pos = pos
        self.score = 0
        self.max_pos = max_pos
        self.die = die
        self.rolls = rolls
        self.target_score = target_score

    def play(self):
        score = sum(next(self.die) for _ in range(self.rolls))
        self.pos = self.wrap(self.pos + score)
        self.score += self.pos

    def wrap(self, pos):
        pos %= self.max_pos
        if pos == 0:
            pos = self.max_pos

        return pos


def solve(lines):
    p1, p2 = parse_input(lines)

    max_pos = 10
    rolls = 3
    target_score = 1000

    d = ddie(100)

    total_rolls = 0

    p1 = Player(p1, max_pos, d, rolls, target_score)
    p2 = Player(p2, max_pos, d, rolls, target_score)

    while True:
    # for _ in range(3):
    #     print(p1.pos, p1.score, p2.pos, p2.score)
        p1.play()
        total_rolls += rolls
        if p1.score >= target_score:
            print(total_rolls, p1.score, p2.score)
            return total_rolls * p2.score

        total_rolls += rolls
        p2.play()
        if p2.score >= target_score:
            print(total_rolls, p1.score, p2.score)
            return total_rolls * p1.score


if __name__ == '__main__':
    utils.solve(solve)

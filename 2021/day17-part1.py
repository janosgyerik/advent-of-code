#!/usr/bin/env python
import math

import utils
import re
from collections import namedtuple, Counter, deque, defaultdict
from itertools import product
from heapq import heappush, heappop, heapify
from functools import lru_cache


class Simulator:
    def __init__(self, x1, x2, y1, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    def find_scoring_aims(self):
        aims = []
        for x in range(self.x2 + 1):
            for y in range(self.y1, -self.y1):
                if self.can_hit_from(x, y):
                    aims.append((x, y))
        return aims

    def can_hit_from(self, vx, vy):
        x = 0
        y = 0
        while x <= self.x2 and self.y1 <= y:
            if self.x1 <= x <= self.x2 and self.y1 <= y <= self.y2:
                return True

            x += vx
            y += vy

            vx = max(0, vx - 1)
            vy -= 1

        return False


def parse_target(line):
    return utils.extract_all_valid_ints(line)


def solve(lines):
    sim = Simulator(*parse_target(lines[0]))

    aims = sim.find_scoring_aims()
    y = max(aim[1] for aim in aims)
    return y * (y + 1) // 2


if __name__ == '__main__':
    utils.solve(solve)

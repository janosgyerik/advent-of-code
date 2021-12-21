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


def nextp(p):
    if p > 10:
        return p - 10
    return p


def compute_wins(p1, p2):
    rolls = {
        3: 1,
        4: 3,
        5: 6,
        6: 7,
        7: 6,
        8: 3,
        9: 1,
    }

    wins1 = 0
    wins2 = 0

    dp = {(p1, 0, p2, 0): 1}

    target = 21

    while dp:
        dp2 = {}
        for state, count in dp.items():
            p1, s1, p2, s2 = state
            for roll, rc in rolls.items():
                p12 = nextp(p1 + roll)
                s12 = s1 + p12
                if s12 >= target:
                    wins1 += count * rc
                else:
                    dp2[p12, s12, p2, s2] = (
                            count * rc
                            # + dp.get((p12, s12, p2, s2), 0)
                            + dp2.get((p12, s12, p2, s2), 0)
                    )

        dp = dp2

        dp2 = {}
        for state, count in dp.items():
            p1, s1, p2, s2 = state
            for roll, rc in rolls.items():
                p22 = nextp(p2 + roll)
                s22 = s2 + p22
                if s22 >= target:
                    wins2 += count * rc
                else:
                    dp2[p1, s1, p22, s22] = (
                            count * rc
                            # + dp.get((p1, s1, p22, s22), 0)
                            + dp2.get((p1, s1, p22, s22), 0)
                    )

        dp = dp2

    return wins1, wins2


def solve(lines):
    p1, p2 = parse_input(lines)

    wins = compute_wins(p1, p2)

    return max(wins), wins


if __name__ == '__main__':
    utils.solve(solve)

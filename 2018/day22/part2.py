#!/usr/bin/env python

import sys
from functools import lru_cache
from heapq import heappush, heappop

MOD = 20183
CFX = 16807
CFY = 48271


@lru_cache(maxsize=None)
def compute_erosion_level(depth, x, y, target):
    if (x, y) in ((0, 0), target):
        v = 0

    elif x == 0:
        v = y * CFY

    elif y == 0:
        v = x * CFX

    else:
        v = compute_erosion_level(depth, x-1, y, target) * compute_erosion_level(depth, x, y-1, target)

    return (v + depth) % MOD


def find_fastest_path(depth, target):
    directions = (1, 0), (0, 1), (-1, 0), (0, -1)
    def valid(x, y):
        return 0 <= x and 0 <= y

    torch, gear, neither = 1, 2, 0
    rocky, wet, narrow = 0, 1, 2
    seen = set()
    q = [(0, 0, 0, torch)]
    while q:
        t, x, y, item = heappop(q)

        if (x, y, item) in seen:
            continue

        seen.add((x, y, item))

        if (x, y) == target:
            if item != torch:
                heappush(q, (t + 7, x, y, torch))
                continue
            return t

        t2 = t + 1
        for dx, dy in directions:
            x2, y2 = x + dx, y + dy
            if not valid(x2, y2):
                continue

            e2 = compute_erosion_level(depth, x2, y2, target) % 3
            if e2 == rocky:
                if item == neither:
                    heappush(q, (t2 + 7, x2, y2, torch))
                    heappush(q, (t2 + 7, x2, y2, gear))
                else:
                    heappush(q, (t2, x2, y2, item))

            elif e2 == wet:
                if item == torch:
                    heappush(q, (t2 + 7, x2, y2, gear))
                    heappush(q, (t2 + 7, x2, y2, neither))
                else:
                    heappush(q, (t2, x2, y2, item))

            elif e2 == narrow:
                if item == gear:
                    heappush(q, (t2 + 7, x2, y2, torch))
                    heappush(q, (t2 + 7, x2, y2, neither))
                else:
                    heappush(q, (t2, x2, y2, item))


def main():
    depth = int(sys.argv[1])
    tx, ty = int(sys.argv[2]), int(sys.argv[3])
    fastest_path = find_fastest_path(depth, (tx, ty))
    print(fastest_path)

if __name__ == '__main__':
    main()

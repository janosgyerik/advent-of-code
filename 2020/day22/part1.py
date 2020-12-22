#!/usr/bin/env python

import sys
from collections import deque


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


class Combat:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def play(self):
        while self.p1.hand and self.p2.hand:
            c1 = self.p1.hand.popleft()
            c2 = self.p2.hand.popleft()
            if c1 < c2:
                self.p2.hand.append(c2)
                self.p2.hand.append(c1)
            else:
                self.p1.hand.append(c1)
                self.p1.hand.append(c2)

    def score(self):
        s1 = self.p1.score()
        s2 = self.p2.score()
        return max(s1, s2)


class Player(object):
    def __init__(self, hand):
        self.hand = deque(hand)

    def score(self):
        s = 0
        for i, x in enumerate(reversed(self.hand)):
            s += (i + 1) * x
        return s


def parse_hands(lines):
    cards = [int(x) for x in lines if x and x[0].isdigit()]
    half = len(cards) // 2
    return Player(cards[:half]), Player(cards[half:])


def main():
    lines = read_lines(sys.argv[1])
    p1, p2 = parse_hands(lines)
    combat = Combat(p1, p2)
    combat.play()
    print(combat.score())


if __name__ == '__main__':
    main()

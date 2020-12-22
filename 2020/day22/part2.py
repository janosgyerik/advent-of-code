#!/usr/bin/env python

import sys
from collections import deque


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


class RecursiveCombat:
    def __init__(self, p1, p2, count=1):
        self.p1 = p1
        self.p2 = p2
        self.seen = set()
        self.count = count

    def play(self):
        while not self.is_over():
            c1 = self.p1.hand.popleft()
            c2 = self.p2.hand.popleft()
            if c1 <= len(self.p1.hand) and c2 <= len(self.p2.hand):
                rp1 = Player([self.p1.hand[i] for i in range(c1)])
                rp2 = Player([self.p2.hand[i] for i in range(c2)])
                r = RecursiveCombat(rp1, rp2, self.count + 1)
                r.play()
                if r.p1.winner:
                    self.p1.hand.append(c1)
                    self.p1.hand.append(c2)
                else:
                    self.p2.hand.append(c2)
                    self.p2.hand.append(c1)

            else:
                if c1 < c2:
                    self.p2.hand.append(c2)
                    self.p2.hand.append(c1)
                else:
                    self.p1.hand.append(c1)
                    self.p1.hand.append(c2)

    def is_over(self):
        if self.is_repeat():
            self.p1.winner = True
            return True

        if not (self.p1.hand and self.p2.hand):
            self.p1.winner = len(self.p1.hand) > 0
            self.p2.winner = len(self.p2.hand) > 0
            return True

        return False

    def is_repeat(self):
        t1 = tuple(self.p1.hand)
        t2 = tuple(self.p2.hand)
        if t1 in self.seen and t2 in self.seen:
            return True

        self.seen.add(t1)
        self.seen.add(t2)
        return False

    def score(self):
        return self.p1.score() if self.p1.winner else self.p2.score()


class Player(object):
    def __init__(self, hand):
        self.hand = deque(hand)
        self.winner = False

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
    combat = RecursiveCombat(p1, p2)
    combat.play()
    print(combat.score())


if __name__ == '__main__':
    main()

#!/usr/bin/env python

import sys
from collections import deque


def compute_high_score(p, m):
    '''
    >>> compute_high_score(9, 25)
    32
    >>> compute_high_score(10, 1618)
    8317
    >>> compute_high_score(13, 7999)
    146373
    >>> compute_high_score(17, 1104)
    2764
    >>> compute_high_score(21, 6111)
    54718
    >>> compute_high_score(30, 5807)
    37305
    >>> compute_high_score(416, 71975)
    439341
    >>> compute_high_score(416, 719750)
    36610911
    >>> compute_high_score(416, 7197500)
    3566801385
    '''
    scores = {i: 0 for i in range(p)}
    marbles = deque([0])
    for marble in range(1, m+1):
        if marble % 23 == 0:
            marbles.rotate(7)
            scores[marble % p] += marble + marbles.pop()
            marbles.rotate(-1)
        else:
            marbles.rotate(-1)
            marbles.append(marble)

    return max(scores.values())

if __name__ == '__main__':
    players = int(sys.argv[1])
    marbles = int(sys.argv[2])
    print(compute_high_score(players, marbles))

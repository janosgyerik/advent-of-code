#!/usr/bin/env python

import sys


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
    '''
    current_index = 0
    scores = {i: 0 for i in range(p)}
    highest = 0
    marbles = [0]
    for marble in range(1, m+1):
        if marble % 23 == 0:
            current_player = marble % p
            scores[current_player] += marble
            current_index = (len(marbles) + current_index - 7) % len(marbles)
            scores[current_player] += marbles[current_index]
            highest = max(highest, scores[current_player])
            del marbles[current_index]
            continue

        current_index += 2
        if current_index < len(marbles):
            marbles.insert(current_index, marble)
            continue

        if current_index == len(marbles):
            marbles.append(marble)
            continue

        current_index = 1
        marbles.insert(current_index, marble)

    return highest

if __name__ == '__main__':
    players = int(sys.argv[1])
    marbles = int(sys.argv[2])
    print(compute_high_score(players, marbles))

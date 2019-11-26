#!/usr/bin/env python

import sys

dxy = {
        'N': (0, -1),
        'S': (0, 1),
        'W': (-1, 0),
        'E': (1, 0),
        }


def count_longest_path(spec):
    '''
    >>> count_longest_path('NWS')
    3
    >>> count_longest_path('NWS|NWSE')
    4
    >>> count_longest_path('NWS(N|WS|S)')
    5
    >>> count_longest_path('ENWWW(NEEE|SSE(EE|N))')
    10
    >>> count_longest_path('ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN')
    18
    >>> count_longest_path('ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))')
    23
    >>> count_longest_path('WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))')
    31
    >>> count_longest_path('NN|N')
    2
    '''
    spec = '({})'.format(spec)
    stack = []
    dists = {}
    x, y = 0, 0
    dist = 0
    for c in spec:
        if c == '(':
            stack.append((x, y, dist))

        elif c == '|':
            x, y, dist = stack[-1]

        elif c == ')':
            x, y, dist = stack.pop()

        elif c in 'NSWE':
            dx, dy = dxy[c]
            x += dx
            y += dy
            pos = x, y
            if pos in dists and dists[pos] < dist + 1:
                dist = dists[pos]
            else:
                dist += 1
                dists[pos] = dist

        else:
            raise ValueError('Unexpected character: {}'.format(c))

    print('paths at least 1000 long:', len([x for x in dists.values() if x >= 1000]))
    return max(dists.values())

if __name__ == '__main__':
    spec = sys.stdin.readline().rstrip()[1:-1]
    print(count_longest_path(spec))

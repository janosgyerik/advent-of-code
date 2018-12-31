#!/usr/bin/env python

import sys, re

re_pos = re.compile(r'^pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)')

pos_list = [[int(x) for x in re_pos.match(line).groups()] for line in sys.stdin.readlines()]

strongest = max(pos_list, key=lambda pos: pos[3])
print(strongest)

def is_within_range(orig, p):
    return sum(abs(orig[i] - p[i]) for i in range(3)) <= orig[3]

within_range = [pos for pos in pos_list if is_within_range(strongest, pos)]
print(len(within_range))

#!/usr/bin/env python

import sys
from collections import namedtuple, Counter, deque, defaultdict
from itertools import product
from heapq import heappush, heappop, heapify
from functools import lru_cache


def ints(line):
    return [int(x) for x in line.split(' ')]


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


def solve(lines):
    count = 0
    prev = float('inf')
    for x in (int(v) for v in lines):
        if prev < x:
            count += 1
        prev = x

    return count


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines))


if __name__ == '__main__':
    main()
#!/usr/bin/env python

fn = 'sample.txt'
fn = 'input.txt'

counts = []

with open(fn) as fh:
    for line in fh.readlines():
        if not counts:
            counts = [[0, 0] for _ in line.rstrip()]

        for i, c in enumerate(line.rstrip()):
            index = 0 if c == '0' else 1
            counts[i][index] += 1

    gamma = 0
    epsilon = 0
    for index in range(len(counts)):
        gamma <<= 1
        epsilon <<= 1

        if counts[index][0] < counts[index][1]:
            gamma += 1
        else:
            epsilon += 1

    print('done', counts, gamma, epsilon, gamma * epsilon)

#!/usr/bin/env python

import sys
from collections import namedtuple, Counter, deque, defaultdict
from itertools import product
from heapq import heappush, heappop, heapify
from functools import lru_cache


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


def make_interval(rspec):
    start, end = rspec.split('-')
    return int(start), int(end)


def build_specs(lines):
    fields = {}
    index = 0

    while True:
        line = lines[index]
        if not line:
            break

        name, rest = line.split(': ')
        r1, _, r2 = rest.split(' ')
        fields[name[:-1]] = make_interval(r1), make_interval(r2)
        index += 1

    mine = [int(x) for x in lines[index+2].split(',')]
    index += 5

    others = [[int(x) for x in line.split(',')] for line in lines[index:]]
    return fields, mine, others


def build_intervals(fields):
    intervals = []
    for pairs in fields.values():
        intervals.extend(pairs)

    return intervals


def within_any_interval(intervals, v):
    for start, end in intervals:
        if start <= v <= end:
            return True

    return False


def find_completely_invalid(fields, others):
    intervals = build_intervals(fields)
    invalid = []
    for other in others:
        for v in other:
            if not within_any_interval(intervals, v):
                invalid.append(v)

    return invalid


def main():
    lines = read_lines(sys.argv[1])
    fields, mine, others = build_specs(lines)
    completely_invalid = find_completely_invalid(fields, others)
    print(sum(completely_invalid))


if __name__ == '__main__':
    main()

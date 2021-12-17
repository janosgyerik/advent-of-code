#!/usr/bin/env python
import re
import sys
from collections import namedtuple, Counter, deque, defaultdict
from itertools import product
from heapq import heappush, heappop, heapify
from functools import lru_cache


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


scoremap = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}


parens = {
    '(': ')',
    '<': '>',
    '[': ']',
    '{': '}',
}


openers = parens.keys()


def find_illegal(s):
    stack = []
    for c in s:
        if c in openers:
            stack.append(c)
        else:
            if not stack:
                return c
            if c != parens[stack[-1]]:
                return c

            stack.pop()


def find_completion(s):
    stack = []
    for c in s:
        if c in openers:
            stack.append(c)
        else:
            if not stack:
                return []
            if c != parens[stack[-1]]:
                return []

            stack.pop()

    return stack


def compute_score(stack):
    score = 0
    while stack:
        score *= 5
        score += scoremap[parens[stack.pop()]]

    return score


def solve(lines):
    scores = []
    for line in lines:
        completion = find_completion(line)
        if completion:
            scores.append(compute_score(completion))

    scores.sort()

    return scores[len(scores) // 2]


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines))


if __name__ == '__main__':
    main()

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


def check_syntax(s):
    """
    Checks the input for unexpected or missing closing characters.
    Returns a pair of detected problems:
    the first value is the first unexpected closing character, if any;
    the second value is the suffix string of missing closing characters, if any.

    Returns (None, None) for a well-formatted string.
    Returns (c, None) for a string where c is the first unexpected closing character.
    Returns (None, suffix) for a string where the suffix would have to be appended to
    make the string well-formed.
    """
    stack = []
    for c in s:
        if c in parens:
            stack.append(parens[c])
        else:
            if not stack or c != stack[-1]:
                return c, None

            stack.pop()

    return None, ''.join(reversed(stack))


def compute_score(suffix):
    score = 0
    for c in suffix:
        score *= 5
        score += scoremap[c]

    return score


def solve(lines):
    scores = []
    for line in lines:
        _, suffix = check_syntax(line)
        if suffix:
            scores.append(compute_score(suffix))

    scores.sort()
    return scores[len(scores) // 2]


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines))


if __name__ == '__main__':
    main()

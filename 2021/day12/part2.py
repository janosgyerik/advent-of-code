#!/usr/bin/env python
import re
import sys
from collections import namedtuple, Counter, deque, defaultdict
from itertools import product
from heapq import heappush, heappop, heapify
from functools import lru_cache


hvd_neighbors = ((-1, 1), (-1, 0), (-1, -1), (0, 1), (0, -1), (1, 1), (1, 0), (1, -1))
hv_neighbors = ((0, 1), (1, 0), (0, -1), (-1, 0))


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


def letters_to_digits(letters):
    return [int(c) for c in letters]


def lines_of_digits_to_grid(lines):
    return [letters_to_digits(line) for line in lines]


class Graph:
    def __init__(self):
        self.adj = defaultdict(set)

    def connect(self, u, v):
        self.adj[u].add(v)
        self.adj[v].add(u)

    def can_re_visit(self, x):
        return x.isupper()

    def can_re_visit_once(self, x):
        return x.islower() and x not in {'start', 'end'}

    def count_paths_from_start_to_end(self):
        return self.count_paths('start', 'end', set(), False)

    def count_paths(self, start, end, visited, visited_twice):
        if start == end:
            return 1

        if start in visited and self.can_re_visit_once(start):
            visited_twice = True

        start_was_in_visited = start in visited
        visited.add(start)

        count = 0
        for v in self.adj[start]:
            if (v not in visited
                    or self.can_re_visit(v)
                    or not visited_twice and self.can_re_visit_once(v)):
                count += self.count_paths(v, end, visited, visited_twice)

        if not start_was_in_visited:
            visited.remove(start)

        return count


def parse_graph(lines):
    g = Graph()
    for line in lines:
        u, v = line.split('-')
        g.connect(u, v)
    return g


def solve(lines):
    g = parse_graph(lines)
    return g.count_paths_from_start_to_end()


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines))


if __name__ == '__main__':
    main()

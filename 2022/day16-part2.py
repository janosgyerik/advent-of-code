#!/usr/bin/env python
import functools
import re
import sys
from collections import namedtuple, Counter, deque, defaultdict
from dataclasses import dataclass, field
from functools import lru_cache
from heapq import heappush, heappop, heapify
from itertools import product
from typing import Callable, List

from utils.binary_search import binary_search


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


def parse_valves(lines):
    template = re.compile(r'Valve (..) has flow rate=(\d+); tunnels? leads? to valves? (.+)')
    graph = {}
    for line in lines:
        groups = template.match(line).groups()
        valve = groups[0]
        rate = int(groups[1])
        neighbors = groups[2].split(', ')
        graph[valve] = (rate, neighbors)

    return graph


class Graph:
    def __init__(self, graph):
        self.graph = graph
        self.indexes = {v: index for index, v in enumerate(graph.keys())}
        self.rates = {0: 0}

        opened = 0
        for u, v in graph.items():
            rate, _ = v
            if rate == 0:
                opened = self.open(opened, u)
        self.opened = opened

        self.all_opened = (1 << len(graph)) - 1

    def compute_pressure(self, opened):
        return self.rates[opened]

    @lru_cache(maxsize=1000000)
    def compute_pressure_from(self, current, minutes, opened):
        if minutes <= 1:
            return 0

        if self.all_open(opened):
            return 0

        rate, neighbors = self.graph[current]

        m = 0
        if not self.is_opened(opened, current):
            m = rate * (minutes - 1) + self.compute_pressure_from(current, minutes - 1, self.open(opened, current))

        for neighbor in neighbors:
            m = max(m, self.compute_pressure_from(neighbor, minutes - 1, opened))

        return m

    def is_opened(self, opened, current):
        index = self.indexes[current]
        return opened & (1 << index) > 0

    def open(self, opened, current):
        index = self.indexes[current]
        oldvalue = self.rates.get(opened, 0)
        opened |= (1 << index)
        self.rates[opened] = oldvalue + self.graph[current][0]
        return opened

    def all_open(self, opened):
        return self.all_opened == opened


def solve(lines, *args):
    g = parse_valves(lines)
    g['AA'][1].remove('GQ')
    g['GQ'][1].remove('AA')
    g['MR'][1].remove('SU')
    g['SU'][1].remove('MR')
    s1 = Graph(g).compute_pressure_from('AA', 26, Graph(g).opened)
    s2 = Graph(g).compute_pressure_from('GQ', 25, Graph(g).opened)
    return s1 + s2


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines, *(sys.argv[2:])))


if __name__ == '__main__':
    main()

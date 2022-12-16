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


def manhattan_distance(sx, sy, bx, by):
    return abs(sx - bx) + abs(sy - by)


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
        self.jammed = {v for v, x in graph.items() if x[0] == 0}
        self.indexes = {}
        index = 0
        for k in graph:
            if k not in self.jammed:
                self.indexes[k] = index
                index += 1
        self.all_opened = (1 << index) - 1
        self.opened = 0

    @lru_cache(maxsize=1000000)
    def compute_pressure_from(self, v1, v2, minutes, opened):
        if minutes <= 1:
            return 0

        if opened == self.all_opened:
            return 0

        rate1, neighbors1 = self.graph[v1]
        rate2, neighbors2 = self.graph[v2]

        m = 0
        # open or move
        # open,open if not at the same
        # open,move
        # move,open
        # move,move
        if self.is_opened(opened, v1) and self.is_opened(opened, v2):
            # both open -> both move
            # move move
            for neighbor1 in neighbors1:
                for neighbor2 in neighbors2:
                    m = max(m, self.compute_pressure_from(neighbor1, neighbor2, minutes - 1, opened))

        elif not self.is_opened(opened, v1) and self.is_opened(opened, v2):
            # open,move
            opened2 = self.open(opened, v1)
            for neighbor2 in neighbors2:
                m = max(m, rate1 * (minutes - 1) + self.compute_pressure_from(v1, neighbor2, minutes - 1, opened2))

            # move move
            for neighbor1 in neighbors1:
                for neighbor2 in neighbors2:
                    m = max(m, self.compute_pressure_from(neighbor1, neighbor2, minutes - 1, opened))

        elif self.is_opened(opened, v1) and not self.is_opened(opened, v2):
            # open,move
            opened2 = self.open(opened, v2)
            for neighbor1 in neighbors1:
                m = max(m, rate2 * (minutes - 1) + self.compute_pressure_from(neighbor1, v2, minutes - 1, opened2))

            # move move
            for neighbor1 in neighbors1:
                for neighbor2 in neighbors2:
                    m = max(m, self.compute_pressure_from(neighbor1, neighbor2, minutes - 1, opened))

        else:
            # both closed

            if v1 != v2:
                # both at different, and they both open
                opened2 = self.open(self.open(opened, v1), v2)
                m = rate1 * (minutes - 1) + rate2 * (minutes - 1)
                m += self.compute_pressure_from(v1, v2, minutes - 1, opened2)
            else:
                # both at the same, one opens, doesn't matter which one
                opened2 = self.open(opened, v2)
                for neighbor1 in neighbors1:
                    m = max(m, rate2 * (minutes - 1) + self.compute_pressure_from(neighbor1, v2, minutes - 1, opened2))

            # move move
            for neighbor1 in neighbors1:
                for neighbor2 in neighbors2:
                    m = max(m, self.compute_pressure_from(neighbor1, neighbor2, minutes - 1, opened))

        return m

    def is_opened(self, opened, current):
        if current in self.jammed:
            return True
        index = self.indexes[current]
        return opened & (1 << index) > 0

    def open(self, opened, current):
        index = self.indexes[current]
        prev = opened
        opened |= (1 << index)
        if prev != opened:
            bits = bin(opened).count('1')
            if self.opened < bits:
                self.opened += 1
                print(bits)
        return opened


def solve(lines, *args):
    g = parse_valves(lines)
    graph = Graph(g)
    return graph.compute_pressure_from('AA', 'AA', 26, 0)


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines, *(sys.argv[2:])))


if __name__ == '__main__':
    main()

#!/usr/bin/env python
import argparse
import itertools
import re
import sys
from collections import namedtuple, Counter, deque, defaultdict
from itertools import product
from heapq import heappush, heappop, heapify
from functools import lru_cache
from numbers import Number
from typing import Callable, Any

hvd_neighbors = ((-1, 1), (-1, 0), (-1, -1), (0, 1), (0, -1), (1, 1), (1, 0), (1, -1))
hv_neighbors = ((0, 1), (1, 0), (0, -1), (-1, 0))

re_int_finder = re.compile(r'(-?\d+)')


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


def solve(solver):
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    lines = read_lines(args.path)
    print(solver(lines))


def int_string_to_digits(s):
    return [int(c) for c in s]


def strings_of_digits_to_grid_of_ints(strings):
    return [int_string_to_digits(s) for s in strings]


def extract_all_valid_ints(s):
    return [int(x) for x in re_int_finder.findall(s)]


def strings_to_int_lists(strings):
    return [extract_all_valid_ints(s) for s in strings]


def delimited_string_to_list(s, delim=None):
    if delim is None:
        return s.split()

    return s.split(delim)


def delimited_strings_to_lists(strings, delim=None):
    return [delimited_string_to_list(s, delim) for s in strings]


# Heavily inspired by https://docs.python.org/3/library/heapq.html#priority-queue-implementation-notes
class PriorityQueue:
    def __init__(self):
        self._pq = []

        # mapping to entries for fast lookup of objects in the queue
        self._items = {}

        # unique object used as a marker
        self._REMOVED = object()

        # unique sequence count to order items by insertion time
        self._counter = itertools.count()

    def add_or_update(self, item, priority: Number = 0):
        """Add a new item or update the priority of an existing item"""
        if item in self._items:
            self.remove(item)
        count = next(self._counter)
        entry = [priority, count, item]
        self._items[item] = entry
        heappush(self._pq, entry)

    def remove(self, item):
        """Mark an existing item as REMOVED. Raise KeyError if not found."""
        entry = self._items.pop(item)
        entry[-1] = self._REMOVED

    def pop(self):
        """Remove and return the lowest priority item. Raise KeyError if empty."""
        while self._pq:
            priority, count, item = heappop(self._pq)
            if item is not self._REMOVED:
                del self._items[item]
                return item

        raise KeyError('pop from an empty priority queue')


class Graph:
    def __init__(self):
        self.adj = defaultdict(set)

    def connect(self, u, v):
        self.adj[u].add(v)
        self.adj[v].add(u)

    def print(self):
        print()


def dijkstra(graph, start, end, weight_getter: Callable[[Any, Any], Number]):
    infinity = float('inf')

    pq = PriorityQueue()
    dist = {}

    for v in graph.adj:
        pq.add_or_update(v, infinity)
        dist[v] = infinity

    pq.add_or_update(start, 0)
    dist[start] = 0

    done = set()

    while pq:
        u = pq.pop()
        if u == end:
            break

        done.add(u)

        for v in graph.adj[u]:
            if v in done:
                continue

            alt = dist[u] + weight_getter(u, v)
            if alt < dist[v]:
                dist[v] = alt
                pq.add_or_update(v, alt)

    return dist[end]


class MatrixPaster:
    def __init__(self, matrix):
        self.matrix = matrix

    def paste_right(self, other):
        pass

    def paste_down(self, other):
        pass

    def update(self, updater):
        pass


class Visitor:
    def pre_visit(self, node):
        pass

    def post_visit(self, node):
        pass

    def get_children(self, node):
        return []

    def stop(self):
        return False


def traverse(node, visitor):
    if visitor.stop():
        return

    visitor.pre_visit(node)

    for child in visitor.get_children(node):
        traverse(child, visitor)

    visitor.post_visit(node)

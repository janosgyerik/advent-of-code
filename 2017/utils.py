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

    def __len__(self):
        return len(self._pq)


class Graph:
    def __init__(self):
        self.adj = defaultdict(set)

    def connect(self, u, v):
        self.adj[u].add(v)
        self.adj[v].add(u)

    def print(self):
        print()

    def connected_components(self):
        uf = UnionFind(len(self.adj))
        for u in self.adj:
            for v in self.adj[u]:
                uf.union(u, v)

        # compress paths
        for u in range(len(self.adj)):
            uf.find(u)

        return uf.root


class UnionFind:
    def __init__(self, n):
        self.root = [-1] * n

    def ensure_capacity(self, size):
        while size >= len(self.root):
            self.root.extend([-1] * len(self.root))

    def union(self, x, y):
        px = self.find(x)
        py = self.find(y)
        self.root[px] = py

    def find(self, x):
        if self.root[x] == -1:
            self.root[x] = x
        elif self.root[x] != x:
            self.root[x] = self.find(self.root[x])

        return self.root[x]


class UnionFindAutoMapper:
    def __init__(self, initial_capacity=1000):
        self.uf = UnionFind(initial_capacity)
        self.count = 0
        self._mapping = {}

    def _map(self, u):
        if u not in self._mapping:
            self._mapping[u] = self.count
            self.count += 1
            self.uf.ensure_capacity(self.count)

        return self._mapping[u]

    def union(self, u, v):
        mu = self._map(u)
        mv = self._map(v)
        self.uf.union(mu, mv)

    def find(self, u):
        return self.uf.find(self._map(u))

    def keys(self):
        return self._mapping.keys()


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


def copy_2d(grid):
    return [row[:] for row in grid]


class Matrix:
    def __init__(self, matrix):
        self.matrix = matrix

    def print(self):
        for row in self.matrix:
            print(' '.join(str(x) for x in row))

        print()

    def copy(self):
        return Matrix(copy_2d(self.matrix))

    def identity(self):
        return Matrix(identity_matrix(len(self.matrix[0])))

    def zero(self):
        matrix = [[0] * len(row) for row in self.matrix]
        return Matrix(matrix)

    def rotations(self):
        rotator = self.identity().matrix
        rotator[0], rotator[1] = rotator[1], rotator[0]
        rotator[0] = [-x for x in rotator[0]]

        for raw_configuration in itertools.permutations(self.identity().matrix, len(rotator)):
            configuration = Matrix(raw_configuration)
            for _ in range(4):
                configuration = configuration.multiply(rotator)
                yield self.multiply(configuration.matrix)

    def multiply(self, rotator):
        result = self.zero().matrix
        dim = len(result[0])

        for r in range(len(result)):
            for c in range(dim):
                total = 0
                for d in range(dim):
                    total += self.matrix[r][d] * rotator[d][c]
                result[r][c] = total
        return Matrix(result)


def identity_matrix(n):
    matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        matrix[i][i] = 1

    return matrix

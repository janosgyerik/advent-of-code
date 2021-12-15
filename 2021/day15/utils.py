#!/usr/bin/env python
import itertools
import re
import sys
from collections import namedtuple, Counter, deque, defaultdict
from itertools import product
from heapq import heappush, heappop, heapify
from functools import lru_cache


hvd_neighbors = ((-1, 1), (-1, 0), (-1, -1), (0, 1), (0, -1), (1, 1), (1, 0), (1, -1))
hv_neighbors = ((0, 1), (1, 0), (0, -1), (-1, 0))

re_int_splitter = re.compile(r'\D+')


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


def int_string_to_digits(s):
    return [int(c) for c in s]


def strings_of_digits_to_grid_of_ints(strings):
    return [int_string_to_digits(s) for s in strings]


def string_to_int_list(s):
    return [int(x) for x in re_int_splitter.split(s)]


def strings_to_int_lists(strings):
    return [string_to_int_list(s) for s in strings]


def delimited_string_to_list(s, delim=None):
    if delim is None:
        return s.split()

    return s.split(delim)


def delimited_strings_to_lists(strings, delim=None):
    return [delimited_string_to_list(s, delim) for s in strings]


class Graph:
    def __init__(self):
        self.adj = defaultdict(set)

    def connect(self, u, v):
        self.adj[u].add(v)
        self.adj[v].add(u)

    def print(self):
        print()

    def cheapest_path(self, start, end, weights=None):
        dist = {}
        q = set()
        for v in self.adj:
            q.add(v)
            if v == start:
                dist[v] = 0
            else:
                dist[v] = float('inf')

        while q:
            print(len(q))
            u = min(q, key=lambda x: dist[x])
            if u == end:
                break

            q.remove(u)

            for v in self.adj[u]:
                if v not in q:
                    continue

                alt = dist[u] + weights[v[0]][v[1]]
                if alt < dist[v]:
                    dist[v] = alt

        return dist[end]

    def cheapest_path2(self, start, end, weights=None):
        pq = []  # list of entries arranged in a heap
        entry_finder = {}  # mapping of tasks to entries
        REMOVED = '<removed-task>'  # placeholder for a removed task
        counter = itertools.count()  # unique sequence count

        def add_task(task, priority=0):
            'Add a new task or update the priority of an existing task'
            if task in entry_finder:
                remove_task(task)
            count = next(counter)
            entry = [priority, count, task]
            entry_finder[task] = entry
            heappush(pq, entry)

        def remove_task(task):
            'Mark an existing task as REMOVED.  Raise KeyError if not found.'
            entry = entry_finder.pop(task)
            entry[-1] = REMOVED

        def pop_task():
            'Remove and return the lowest priority task. Raise KeyError if empty.'
            while pq:
                priority, count, task = heappop(pq)
                if task is not REMOVED:
                    del entry_finder[task]
                    return task
            raise KeyError('pop from an empty priority queue')

        dist = {}
        for v in self.adj:
            if v == start:
                add_task(v, 0)
                dist[v] = 0
            else:
                add_task(v, float('inf'))
                dist[v] = float('inf')

        done = set()

        while pq:
            u = pop_task()
            if u == end:
                break

            done.add(u)

            for v in self.adj[u]:
                if v in done:
                    continue

                alt = dist[u] + weights[v[0]][v[1]]
                if alt < dist[v]:
                    dist[v] = alt
                    add_task(v, alt)

        return dist[end]


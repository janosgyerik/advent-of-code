#!/usr/bin/env python
import math

import utils
import re
from collections import namedtuple, Counter, deque, defaultdict
from itertools import product
from heapq import heappush, heappop, heapify
from functools import lru_cache


def parse_nodes(lines):
    arrow = ' -> '
    for line in lines:
        if arrow in line:
            left, right = line.split(arrow)
            children = right.split(', ')
        else:
            left = line
            children = []

        name = left.split()[0]
        weight = utils.extract_all_valid_ints(left)[0]
        yield name, weight, children


class Node:
    def __init__(self, name, weight, children):
        self.name = name
        self.weight = weight
        self.children = children


def parse_tree(nodes):
    cache = {}
    dependents = set()
    for name, weight, children in nodes:
        cache[name] = Node(name, weight, children)
        dependents.update(children)

    for name in cache:
        if name not in dependents:
            return name, cache


def solve(lines):
    root, nodes = parse_tree(parse_nodes(lines))

    ans = [None]

    def check_children(name):
        if ans[0] is not None:
            return

        node = nodes[name]
        if not node.children:
            return node.weight

        weights = []
        for child in node.children:
            weights.append((child, check_children(child)))
            if ans[0] is not None:
                return

        heaviest = max(weights, key=lambda x: x[1])
        typical = min(weights, key=lambda x: x[1])
        diff = heaviest[1] - typical[1]
        if diff:
            heavy = nodes[heaviest[0]]
            ans[0] = heavy.weight - diff

        return node.weight + sum(x[1] for x in weights)

    check_children(root)

    return ans[0]


if __name__ == '__main__':
    utils.solve(solve)

#!/usr/bin/env python
import math

import utils
import re
from collections import namedtuple, Counter, deque, defaultdict
from itertools import product
from heapq import heappush, heappop, heapify
from functools import lru_cache


class Parser:
    def __init__(self, s):
        self.s = s
        self.index = 0
        self.n = len(s)

    def parse(self):
        self.skip('[')

        if self.peek() == '[':
            left = self.parse()
        else:
            left = SnailFish(self.parse_int())

        self.skip(',')

        if self.peek() == '[':
            right = self.parse()
        else:
            right = SnailFish(self.parse_int())

        self.skip(']')

        sf = SnailFish(None, left, right)
        sf.left.parent = sf
        sf.right.parent = sf
        return sf

    def peek(self):
        return self.s[self.index]

    def pop(self):
        self.index += 1
        return self.s[self.index - 1]

    def skip(self, expected):
        assert self.s[self.index] == expected
        self.index += 1

    def parse_int(self):
        assert '0' <= self.s[self.index] <= '9'
        return int(self.pop())


def parse_snailfish(s):
    return Parser(s).parse()


class ToExplodeFinderVisitor(utils.Visitor):
    def __init__(self):
        self.prev = None
        self.to_explode = None
        self.left = None
        self.right = None
        self.height = 0
        self.result = [None, None, None]

    def get_children(self, node):
        if node.val is not None:
            return []

        if node is self.to_explode:
            return []

        return [node.left, node.right]

    def pre_visit(self, node):
        self.height += 1

        if self.height == 5 and node.val is None:
            if self.to_explode is None:
                self.left = self.result[0] = self.prev
                self.to_explode = self.result[1] = node
                return

        if node.val is not None:
            if self.to_explode is not None:
                self.right = self.result[2] = node
                return

            self.prev = node

    def post_visit(self, node):
        self.height -= 1

    def stop(self):
        return self.right is not None


def find_to_explode(node):
    visitor = ToExplodeFinderVisitor()
    utils.traverse(node, visitor)
    return visitor.result


class SnailFish:
    def __init__(self, val, left=None, right=None):
        self.parent = None
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        if self.val is not None:
            return str(self.val)

        return f'[{self.left},{self.right}]'

    def print(self, indent=0):
        if self.val is not None:
            print('  ' * indent + str(self.val))
            return

        print('  ' * indent + '.')
        indent += 1
        self.left.print(indent)
        self.right.print(indent)

    def add(self, other):
        sf = SnailFish(None, self, other)
        sf.left.parent = sf
        sf.right.parent = sf
        sf.reduce()
        return sf

    def reduce(self):
        while True:
            left, to_explode, right = find_to_explode(self)

            if to_explode is None:
                to_split = self.find_to_split()
                if not to_split:
                    break

                left = SnailFish(to_split.val // 2)
                right = SnailFish(math.ceil(to_split.val / 2))
                sf = SnailFish(None, left, right)
                left.parent = sf
                right.parent = sf

                parent = to_split.parent
                sf.parent = parent
                if parent.left is to_split:
                    parent.left = sf
                else:
                    parent.right = sf

                continue

            if left:
                left.val += to_explode.left.val

            if right:
                right.val += to_explode.right.val

            parent = to_explode.parent
            sf = SnailFish(0)
            sf.parent = parent
            if parent.left is to_explode:
                parent.left = sf
            else:
                parent.right = sf

    def find_to_split(self):
        if self.val is not None:
            if self.val >= 10:
                return self

        else:
            found = self.left.find_to_split()
            if found:
                return found

            return self.right.find_to_split()


def compute_sum(nums):
    total = nums[0]
    for num in nums[1:]:
        total = total.add(num)

    return total


def magnitude(node):
    if node.val is not None:
        return node.val

    return 3 * magnitude(node.left) + 2 * magnitude(node.right)


def solve(lines):
    nums = [parse_snailfish(line) for line in lines]
    total = compute_sum(nums)
    return magnitude(total)


if __name__ == '__main__':
    utils.solve(solve)

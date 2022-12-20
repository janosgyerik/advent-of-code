#!/usr/bin/env python
import functools
import re
import sys
from collections import namedtuple, Counter, deque, defaultdict
from dataclasses import dataclass, field
from functools import lru_cache
from heapq import heappush, heappop, heapify
from itertools import product
from typing import Callable, List, Set, Tuple

from utils.binary_search import binary_search
from utils import parsing
from utils import coordinates
from enum import Enum, auto


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


def parse_nums(lines):
    for line in lines:
        yield int(line)


class ListNode:
    def __init__(self, val):
        self.val = val
        self.next = None
        self.prev = None
        self.rotated = False


class CircularList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
        self.zero = None

    def append(self, val):
        node = ListNode(val)
        if val == 0:
            self.zero = node

        self.size += 1

        if self.head is None:
            self.head = self.tail = node
            node.next = node
            node.prev = node

        else:
            self.tail.next = node
            node.prev = self.tail
            self.tail = node
            self.tail.next = self.head
            self.head.prev = self.tail

    def print(self):
        node = self.head
        for _ in range(self.size):
            print(node.val)
            node = node.next
        print()

    def mix(self, count):
        to_mix = []
        node = self.head
        for _ in range(self.size):
            to_mix.append(node)
            node = node.next

        for _ in range(count):
            for node in to_mix:
                self.move(node)

    def move(self, node):
        pos = node.val

        if pos >= 0:
            pos %= self.size - 1
        else:
            pos = -(-pos % (self.size - 1))

        if not pos:
            return

        self.remove(node)

        if pos > 0:
            node2 = node.next
            for _ in range(pos - 1):
                node2 = node2.next

            node.next = node2.next
            node.next.prev = node
            node.prev = node2
            node.prev.next = node

        else:
            node2 = node.prev
            for _ in range(-pos):
                node2 = node2.prev

            node.next = node2.next
            node.next.prev = node
            node.prev = node2
            node.prev.next = node

        self.tail = self.head.prev

    def get(self, pos):
        pos %= self.size
        node = self.zero
        for _ in range(pos):
            node = node.next

        return node.val

    def remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

        if self.head == node:
            self.head = node.next

        elif self.tail == node:
            self.tail = node.prev


def make_list(nums):
    lst = CircularList()
    for num in nums:
        lst.append(num)

    assert lst.tail.next == lst.head
    assert lst.head.prev == lst.tail

    return lst


def solve(lines, *args):
    nums = list(parse_nums(lines))
    nums = [num * 811589153 for num in nums]

    lst = make_list(nums)
    lst.mix(10)
    lst.print()
    print(lst.get(1000))
    print(lst.get(2000))
    print(lst.get(3000))

    return sum([lst.get(1000), lst.get(2000), lst.get(3000)])


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines, *(sys.argv[2:])))


if __name__ == '__main__':
    main()

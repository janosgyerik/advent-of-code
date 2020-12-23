#!/usr/bin/env python

import sys


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None


class Deque:
    def __init__(self):
        self.head = self.tail = None

    def append(self, value):
        node = Node(value)
        if not self.head:
            self.head = self.tail = node
        else:
            node.next = self.head
            node.prev = self.tail
            self.tail.next = node
            self.head.prev = node
            self.tail = node

        return node

    def rotate(self):
        self.tail = self.head
        self.head = self.head.next

    def popleft(self):
        value = self.head.value
        self.head = self.head.next
        self.tail.next = self.head
        self.head.prev = self.tail
        return value

    def insert_after(self, node, value):
        node2 = Node(value)
        node2.next = node.next
        node2.prev = node
        node2.prev.next = node2
        node2.next.prev = node2
        return node2


class HashDeque:
    def __init__(self, values):
        self.nodes = {}
        self.deque = Deque()
        for value in values:
            self.append(value)

    def append(self, value):
        self.nodes[value] = self.deque.append(value)

    def first(self):
        return self.deque.head.value

    def rotate(self):
        self.deque.rotate()

    def popleft(self):
        return self.deque.popleft()

    def insert_after_value(self, value, values):
        node = self.nodes[value]
        for v in values:
            node = self.deque.insert_after(node, v)
            self.nodes[v] = node

    def two_values_after(self, value):
        node = self.nodes[value]
        return node.next.value, node.next.next.value


class CrabCups:
    def __init__(self, cups):
        self.cups = HashDeque(cups)
        self.max = max(cups)

    def play(self):
        current = self.cups.first()

        self.cups.rotate()
        removed = []
        for _ in range(3):
            removed.append(self.cups.popleft())

        destination = current - 1
        if destination == 0:
            destination = self.max
        while destination in removed:
            destination -= 1
            if destination == 0:
                destination = self.max

        self.cups.insert_after_value(destination, removed)

    def play_n(self, n):
        for _ in range(n):
            self.play()

    def score(self):
        x, y = self.cups.two_values_after(1)
        return x * y


def main():
    lines = read_lines(sys.argv[1])
    cups = [int(x) for x in lines[0]] + list(range(10, 10 ** 6 + 1))
    crabcups = CrabCups(cups)
    crabcups.play_n(10 ** 7)
    print(crabcups.score())


if __name__ == '__main__':
    main()

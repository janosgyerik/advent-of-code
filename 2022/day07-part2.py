#!/usr/bin/env python

import sys
from collections import namedtuple, Counter, deque, defaultdict
from dataclasses import dataclass
from functools import lru_cache
from heapq import heappush, heappop, heapify
from itertools import product


def ints(line):
    return [int(x) for x in line.split(' ')]


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


class TreeNode:
    def __init__(self, name, size=0):
        self.name = name
        self.size = size
        self.children = {}
        self.parent = None

    def get_or_create(self, name):
        if name in self.children:
            return self.children[name]

        return self.add_child(name, 0)

    def add_child(self, name, size):
        child = TreeNode(name, size)
        child.parent = self
        self.children[name] = child
        return child


class FS:
    def __init__(self):
        self.root = TreeNode('/')
        self.cwd = self.root

    def cd(self, dirname):
        if dirname == '/':
            self.cwd = self.root
        elif dirname == '..':
            self.cwd = self.cwd.parent
        else:
            self.cwd = self.cwd.get_or_create(dirname)

    def add_file(self, filename, size):
        self.cwd.add_child(filename, size)

    def print(self):
        def p(node, indent):
            if node.size == 0:
                stats = '(dir)'
            else:
                stats = f'(file, size={node.size})'

            print(f'{indent}- {node.name} {stats}')
            for _, child in node.children.items():
                p(child, indent + '  ')

        p(self.root, '')


def compute_sizes(node, acc):
    size = 0
    if node.size == 0:
        for _, child in node.children.items():
            compute_sizes(child, acc)
            size += child.size
        node.size = size

    acc.append(size)


def solve(lines):
    linenum = 0
    fs = FS()
    while linenum < len(lines):
        line = lines[linenum]
        if line.startswith('$ cd'):
            fs.cd(line[5:])
            linenum += 1
        elif line == '$ ls':
            while linenum + 1 < len(lines):
                linenum += 1
                if lines[linenum].startswith('$ '):
                    break

                line = lines[linenum]
                parts = line.split()
                if parts[0] != 'dir':
                    size, filename = parts
                    size = int(size)
                    fs.add_file(filename, size)
            else:
                linenum += 1

        else:
            raise ValueError(f'Unexpected input: {line}')

    acc = []
    compute_sizes(fs.root, acc)

    maxdisk = 70000000
    maxused = maxdisk - 30000000
    to_free = fs.root.size - maxused
    to_delete = min(x for x in acc if x >= to_free)
    return to_delete


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines))


if __name__ == '__main__':
    main()

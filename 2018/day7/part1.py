#!/usr/bin/env python

import sys, re
from collections import namedtuple
from heapq import heappush, heappop, heapify

Link = namedtuple('Link', ['src', 'dst'])


class Graph:
    def __init__(self, links):
        self.nodes = {}
        self.deps = {}
        self.links = links
        self.ids = set(link.src for link in self.links)
        nonroot = set()
        for link in self.links:
            nonroot.add(link.dst)
            if link.src in self.nodes:
                self.nodes[link.src].append(link)
            else:
                self.nodes[link.src] = [link]
            if link.dst in self.deps:
                self.deps[link.dst].append(link.src)
            else:
                self.deps[link.dst] = [link.src]

        self.roots = [x for x in self.ids if x not in nonroot]

    def compute_instructions(self):
        done = set()
        instructions = ""
        heap = list(self.roots)
        heapify(heap)
        while heap:
            next_instruction = heappop(heap)
            done.add(next_instruction)
            instructions += next_instruction
            if next_instruction in self.nodes:
                for link in self.nodes[next_instruction]:
                    if all(dep in done for dep in self.deps[link.dst]):
                        heappush(heap, link.dst)

        return instructions

    def display(self):
        for link in self.links:
            print(link)
        print(self.nodes)
        print(self.deps)
        print(self.roots)


links = [Link(src, dst) for src, dst in
        [re.findall(r'(.) must be finished before step (.)', line)[0] for line in sys.stdin.readlines()]]

graph = Graph(links)
graph.display()
print(graph.compute_instructions())

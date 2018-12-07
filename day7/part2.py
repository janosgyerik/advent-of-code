#!/usr/bin/env python

import sys, re
from collections import defaultdict
from heapq import heappush, heappop, heapify


def compute_t(label, base):
    '''
    >>> compute_t('A', 0)
    1
    >>> compute_t('C', 0)
    3
    >>> compute_t('C', 60)
    63
    '''
    return base + ord(label) - ord('A') + 1


class Graph:
    def __init__(self, links):
        self.nodes = defaultdict(list)
        self.deps = defaultdict(list)
        self.ids = set(src for src, _ in links)
        nonroots = set()
        for src, dst in links:
            nonroots.add(dst)
            self.nodes[src].append(dst)
            self.deps[dst].append(src)

        self.roots = [x for x in self.ids if x not in nonroots]

    def compute_time(self, workers_cnt, base):
        done = {}
        workers = [0] * workers_cnt
        heap = [(0, x) for x in self.roots]
        heapify(heap)
        while heap:
            t_start, next_instruction = heappop(heap)
            t_start = max(t_start, heappop(workers))
            t_done = t_start + compute_t(next_instruction, base)
            heappush(workers, t_done)

            if next_instruction not in self.nodes:
                break

            done[next_instruction] = t_done

            for dst in self.nodes[next_instruction]:
                if all(dep in done for dep in self.deps[dst]):
                    heappush(heap, (t_done, dst))

        return t_done

if __name__ == '__main__':
    links = [re.findall(r'(.) must be finished before step (.)', line)[0] for line in sys.stdin.readlines()]

    graph = Graph(links)
    workers_cnt = int(sys.argv[1])
    base = int(sys.argv[2])
    print(graph.compute_time(workers_cnt, base))

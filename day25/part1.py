#!/usr/bin/env python

import sys


class SpaceTime:
    def __init__(self, points):
        self.points = points

    def count_consellations(self):
        constellations = {}

        def dist(p1, p2):
            return sum([abs(p1[i] - p2[i]) for i in range(len(p1))])

        def merge(c1, c2):
            merged = c1.union(c2)
            for p in merged:
                constellations[p] = merged
            return merged

        for p1 in self.points:
            c1 = constellations.get(p1, set())
            if not c1:
                c1.add(p1)
                constellations[p1] = c1

            for p2, c2 in constellations.items():
                if p1 == p2:
                    continue

                if dist(p1, p2) <= 3:
                    c1 = merge(c1, c2)

        to_count = set(self.points)
        count = 0
        while to_count:
            count += 1
            p1 = to_count.pop()
            constellations[p1].remove(p1)
            for p2 in constellations[p1]:
                to_count.remove(p2)

        return count

if __name__ == '__main__':
    points = [tuple([int(x) for x in line.strip().split(',')])
            for line in sys.stdin.readlines()]
    st = SpaceTime(points)
    print(st.count_consellations())

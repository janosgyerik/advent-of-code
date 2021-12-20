#!/usr/bin/env python
import math

import utils
import re
from collections import namedtuple, Counter, deque, defaultdict
from itertools import product
from heapq import heappush, heappop, heapify
from functools import lru_cache


REQUIRED = 12
MAXSHIFT = 1000


def parse_scanners(lines):
    scanners = []
    beacons = []
    lines.append('')

    for line in lines:
        if not line:
            scanners.append(Scanner(beacons))
            beacons = []
        elif 'scanner' not in line:
            beacons.append(utils.extract_all_valid_ints(line))

    return scanners


class Scanner:
    seq = (x for x in range(1000))

    def __init__(self, beacons):
        self.beacons = beacons
        self.aligned = False
        self.checked = False
        self.index = next(Scanner.seq)

    def print(self):
        for beacon in self.beacons:
            print(','.join(str(x) for x in beacon))
        print()

    def rotate(self, rotator):
        self.beacons = [utils.Matrix([b]).multiply(rotator).matrix[0] for b in self.beacons]

    def matches(self, other):
        required = REQUIRED
        maxshift = MAXSHIFT * 2 + 1
        x1 = {x for x, y, z in self.beacons}
        xy1 = {(x, y) for x, y, z in self.beacons}
        xyz1 = {(x, y, z) for x, y, z in self.beacons}

        for dx in range(-maxshift, maxshift):
            x2 = {x + dx for x, y, z in other.beacons}
            if len(x1.intersection(x2)) >= required:
                for dy in range(-maxshift, maxshift):
                    xy2 = {(x + dx, y + dy) for x, y, z in other.beacons}
                    if len(xy1.intersection(xy2)) >= required:
                        for dz in range(-maxshift, maxshift):
                            xyz2 = {(x + dx, y + dy, z + dz) for x, y, z in other.beacons}
                            if len(xyz1.intersection(xyz2)) >= required:
                                other.beacons = [(x + dx, y + dy, z + dz) for x, y, z in other.beacons]
                                return True

        return False


def count_unique_beacons(scanners):
    beacons = set()
    for s in scanners:
        for b in s.beacons:
            beacons.add(tuple(b))

    # counts = Counter()
    # for s in scanners:
    #     for b in s.beacons:
    #         counts[tuple(b)] += 1
    #
    # for t in sorted(counts.keys()):
    #     print(t, counts[t])

    return len(beacons)


def find_aligned_unchecked(scanners):
    for i, s in enumerate(scanners):
        if s.aligned and not s.checked:
            return i, s

    return None, None


def align_scanners(scanners):
    def helper(pivot):
        scanners[pivot].aligned = True

        rotations = list(utils.Matrix(utils.identity_matrix(3)).rotations())
        for i in range(len(rotations)):
            negated = [[-x for x in row] for row in rotations[i].matrix]
            rotations.append(utils.Matrix(negated))

        for _ in range(len(scanners)):
            i1, s1 = find_aligned_unchecked(scanners)
            if not s1:
                break

            for i2, s2 in enumerate(scanners):
                if s2.aligned:
                    continue

                orig = utils.copy_2d(s2.beacons)
                for r in rotations:
                    s2.beacons = orig[:]
                    s2.rotate(r.matrix)
                    if s1.matches(s2):
                        s2.aligned = True
                        break

            s1.checked = True

    orig = [s.beacons for s in scanners]

    for pivot in range(len(scanners)):
        print('testing pivot', pivot)
        for i, s in enumerate(scanners):
            scanners[i] = Scanner(orig[i][:])

        helper(pivot)
        print(count_unique_beacons(scanners))
        if all(s.aligned for s in scanners):
            return


def count_beacons(scanners):
    """
    align all scanners, based on the pattern of the detected beacons

    compute the coordinates of the scanners

    count the unique beacons, based on the scanner coordinates + relative beacon coordinates

    how to align the scanners?

    scanner states:
    - matched: it is aligned and checked all others for alignment
    - checking: it was aligned when visiting another scanner, but it did not check all others
    - unmatched

    for each checking scanner s1
        for each other checking s2
            if have at least 12 in common -> set coordinates

        for each other unmatched s2
            for each rotation of s2
                if have at least 12 in common -> set coordinates, mark as checking, stop rotating

        mark as checked

    how to check if two scanners have 12 overlap?
    - too hard when not aligned
    - that's why we rotate!
    - sort beacons by coordinates x, y, z
    -

    for every xshift such that there are at least 12 x in common
        for every yshift such that there are at least 12 y in common
            find a zshift such that there are at least 12 z in common
    else skip
    """
    align_scanners(scanners)
    return count_unique_beacons(scanners)


def solve(lines):
    scanners = parse_scanners(lines)

    def dist(p1, p2):
        return sum((p1[i] - p2[i])**2 for i in range(3))

    for s in scanners:
        pairs = 0
        dists = set()
        dists_to_points = {}
        for i1, b1 in enumerate(s.beacons):
            for i2 in range(i1 + 1, len(s.beacons)):
                b2 = s.beacons[i2]
                d = dist(b1, b2)
                dists.add(d)
                pairs += 1
                dists_to_points[d] = (i1, i2)

        s.dists = dists
        s.dists_to_points = dists_to_points
        s.counts = Counter()

    matched = set()
    for s1 in scanners:
        for s2 in scanners:
            if s1 is s2:
                continue

            points1 = set()
            points2 = set()
            for d in s1.dists.intersection(s2.dists):
                points1.update(s1.dists_to_points[d])
                points2.update(s2.dists_to_points[d])

            for p in points1:
                s1.counts[p] += 1
            for p in points2:
                s2.counts[p] += 1

            if len(points1) >= 12:
                print('match', s1.index, s2.index, len(s1.dists.intersection(s2.dists)))
                matched.add(s1.index)
                matched.add(s2.index)

    for s in scanners:
        print(s.counts)

    print(sum(sum(1 for v in s.counts.values()) for s in scanners))

    return 1
    return count_beacons(scanners)


if __name__ == '__main__':
    utils.solve(solve)

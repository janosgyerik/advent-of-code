#!/usr/bin/env python
import itertools
import math

import utils
import re
from collections import namedtuple, Counter, deque, defaultdict
from itertools import product
from heapq import heappush, heappop, heapify
from functools import lru_cache


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
    counter = itertools.count()

    def __init__(self, beacons):
        self.beacons = beacons
        self.aligned = False
        self.checked = False
        self.index = next(Scanner.counter)

    def print(self):
        for beacon in self.beacons:
            print(','.join(str(x) for x in beacon))
        print()

    def rotate(self, rotator):
        self.beacons = [utils.Matrix([b]).multiply(rotator).matrix[0] for b in self.beacons]

    def matches(self, other):
        required = 12
        maxshift = 2000
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

    def apply_shift(self, dx, dy, dz):
        for b in self.beacons:
            b[0] += dx
            b[1] += dy
            b[2] += dz


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
    # print(counts)

    return len(beacons)


def find_aligned_unchecked(scanners):
    for i, s in enumerate(scanners):
        if s.aligned and not s.checked:
            return i, s

    return None, None


def align_scanners1(scanners):
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


def compute_dist(b1, b2):
    return sum((a - b)**2 for a, b in zip(b1, b2))


def compute_and_verify_unique_distances(scanner):
    dists = {}
    for i1, b1 in enumerate(scanner.beacons):
        for i2 in range(i1 + 1, len(scanner.beacons)):
            b2 = scanner.beacons[i2]
            dist = compute_dist(b1, b2)
            assert dist not in dists
            dists[dist] = (i1, i2)

    return dists


def align_scanners(scanners):
    """
    match scanners by matching distances between beacons
    this assumes that for each scanner, the distances between the beacons
    they see is unique -> verified
    """
    for s in scanners:
        s.dists = compute_and_verify_unique_distances(s)
        s.dists_keys = set(s.dists.keys())

    """
    if two scanners have 66 = 12 * 11 / 2 overlapping distances -> they match
    
    build a graph from connected scanners
    """
    g = utils.Graph()
    for i1, s1 in enumerate(scanners):
        for i2 in range(i1 + 1, len(scanners)):
            s2 = scanners[i2]
            if len(s1.dists_keys.intersection(s2.dists_keys)) >= 66:
                g.connect(i1, i2)

    """
    starting from any scanner,
    align it with all its un-aligned neighbors, DFS
    """
    aligned = set()

    def align_neighbors(u):
        aligned.add(u)

        for v in g.adj[u]:
            if v not in aligned:
                align_matched_scanners(scanners[u], scanners[v])
                align_neighbors(v)

    # for i1 in range(len(scanners)):
    #     align_neighbors(i1)
    align_neighbors(0)

    # aligned.add(13)
    # aligned.add(17)
    # aligned.add(24)
    # for s in scanners:
    #     if s.index not in aligned:
    #         print('not aligned!', s.index)
    #         for s2 in scanners:
    #             if s2 == s:
    #                 continue
    #
    #             z = len(s.dists_keys.intersection(s2.dists_keys))
    #             print('intersections with', s2.index, z)
    #
    #         break

    assert len(aligned) == len(scanners)


def align_matched_scanners(s1, s2):
    """
    find the rotation and shift to align s2 with s1

    find the common points

    sort the common points of s1 by x, y, z

    for each rotation:
        apply next rotation on s2

        sort the common points of s2 by x, y, z

        if the dist between the pairwise sorted points is the same,
        then break

    at this point the points are aligned along the same orientation,
    and possibly there is a shift;
    the shift is equal to the difference vector between any pairwise points

    apply the shift to all points in s2
    """
    common_dists = s1.dists_keys.intersection(s2.dists_keys)
    assert len(common_dists) >= 66

    def collect_matched_point_indexes(scanner):
        counts = Counter()
        for dist in common_dists:
            p1, p2 = scanner.dists[dist]
            counts[p1] += 1
            counts[p2] += 1

        return [k for k, v in counts.items() if v > 1]

    def to_points(scanner, indexes):
        return sorted([scanner.beacons[index] for index in indexes])

    p1_indexes = collect_matched_point_indexes(s1)
    p2_indexes = collect_matched_point_indexes(s2)
    assert len(p1_indexes) == len(p2_indexes)
    assert len(p1_indexes) == 12, f'expected 12 common points, got {len(p1_indexes)}'

    p1s = to_points(s1, p1_indexes)

    rotations = list(utils.Matrix(utils.identity_matrix(3)).rotations())
    for i in range(len(rotations)):
        negated = [[-x for x in row] for row in rotations[i].matrix]
        rotations.append(utils.Matrix(negated))

    orig = utils.copy_2d(s2.beacons)
    for r in rotations:
        s2.beacons = orig[:]
        s2.rotate(r.matrix)
        p2s = to_points(s2, p2_indexes)
        d0 = compute_dist(p1s[0], p2s[0])
        for i in range(1, len(p2s)):
            d = compute_dist(p1s[i], p2s[i])
            if d != d0:
                break
        else:
            break
    else:
        assert False, f'No matching rotation for {s1.index} and {s2.index} ;-('

    dx, dy, dz = [a - b for a, b in zip(p1s[0], p2s[0])]
    s2.apply_shift(dx, dy, dz)

    # after alignment, there must be at least 12 matching points
    verify_alignment(s1, s2)


def verify_alignment(s1, s2):
    b1 = {tuple(b) for b in s1.beacons}
    count = 0
    for b in s2.beacons:
        if tuple(b) in b1:
            count += 1
            if count == 12:
                return

    assert False, f"expected at least 12 matching beacons; got {count}"


def solve(lines):
    scanners = parse_scanners(lines)
    align_scanners(scanners)
    return count_unique_beacons(scanners)


if __name__ == '__main__':
    utils.solve(solve)

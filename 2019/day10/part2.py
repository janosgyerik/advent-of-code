#!/usr/bin/env python3

import sys


def sign(v):
    if v == 0:
        return 0
    if v > 0:
        return 1
    return -1


def direction(a, b):
    return sign(b[0] - a[0]), sign(a[1] - b[1])


def angle(a, b):
    d = direction(a, b)
    if a[0] == b[0]:
        return d, 0
    if a[1] == b[1]:
        return d, 0
    return d, (b[0] - a[0]) / (b[1] - a[1])


def angles(asteroids, a):
    return [(b, angle(a, b)) for b in asteroids]


def unique_angle_count(asteroids, a):
    return len(set(angle(a, b) for b in asteroids))


def find_asteroids(lines):
    for r in range(len(lines)):
        for c, v in enumerate(lines[r]):
            if v != '.':
                yield c, r


def sq(v):
    return v * v


def distance(a, b):
    return sq(a[0] - b[0]) + sq(a[1] - b[1])


def main():
    lines = [x.rstrip() for x in sys.stdin.readlines()]
    asteroids = list(find_asteroids(lines))
    station, count = max(((a, unique_angle_count(asteroids, a)) for a in asteroids), key=lambda x: x[1])
    print(station, count)

    # eliminate unreachable: group by angle, keep only closest
    closest_by_angle = {}
    for ang in angles(asteroids, station):
        if ang[1] in closest_by_angle:
            if distance(station, ang[0]) < distance(station, closest_by_angle[ang[1]][0]):
                closest_by_angle[ang[1]] = ang
        else:
            closest_by_angle[ang[1]] = ang

    directions = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 0)]
    direction_order = {d: i for i, d in enumerate(directions)}

    # sort by direction and then angle
    def ordering(v):
        _, (d, angle) = v
        return direction_order[d], -angle

    seq = sorted(closest_by_angle.values(), key=ordering)
    print(seq[199][0])


if __name__ == '__main__':
    main()

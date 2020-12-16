#!/usr/bin/env python

import sys
from functools import reduce


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


def make_interval(rspec):
    start, end = rspec.split('-')
    return int(start), int(end)


def build_specs(lines):
    fields = {}
    index = 0

    while True:
        line = lines[index]
        if not line:
            break

        name, rest = line.split(': ')
        r1, _, r2 = rest.split(' ')
        fields[name] = make_interval(r1), make_interval(r2)
        index += 1

    mine = [int(x) for x in lines[index+2].split(',')]
    index += 5

    others = [[int(x) for x in line.split(',')] for line in lines[index:]]
    return fields, mine, others


def build_intervals(fields):
    intervals = []
    for pairs in fields.values():
        intervals.extend(pairs)

    return intervals


def within_any_interval(intervals, v):
    for start, end in intervals:
        if start <= v <= end:
            return True

    return False


def find_completely_invalid(fields, others):
    intervals = build_intervals(fields)
    invalid = []
    for other in others:
        for v in other:
            if not within_any_interval(intervals, v):
                invalid.append(v)

    return invalid


def is_possibly_valid(intervals, ticket):
    for v in ticket:
        if not within_any_interval(intervals, v):
            return False

    return True


def is_possible_index(tickets, index, intervals):
    for ticket in tickets:
        for start, end in intervals:
            if start <= ticket[index] <= end:
                break
        else:
            return False

    return True


def find_mapping(fields, mine, others):
    intervals = build_intervals(fields)
    tickets = [mine] + [ticket for ticket in others if is_possibly_valid(intervals, ticket)]

    positions = set(range(len(mine)))
    candidates = {name: positions.copy() for name in fields.keys()}
    mapping = {}
    while candidates:
        candidates2 = {name: set() for name in candidates.keys()}
        for name, indexes in candidates.items():
            for index in indexes:
                if is_possible_index(tickets, index, fields[name]):
                    candidates2[name].add(index)

        candidates3 = {}
        for name, indexes in candidates2.items():
            if len(indexes) == 1:
                pos = list(indexes)[0]
                mapping[name] = pos
                positions.remove(pos)
            else:
                candidates3[name] = indexes

        candidates = {name: {pos for pos in indexes if pos in positions}
                      for name, indexes in candidates3.items()}

    return mapping


def main():
    lines = read_lines(sys.argv[1])
    fields, mine, others = build_specs(lines)
    completely_invalid = find_completely_invalid(fields, others)
    print(sum(completely_invalid))

    mapping = find_mapping(fields, mine, others)
    departure_positions = [index for name, index in mapping.items() if name.startswith('depart')]
    departure_values = [mine[index] for index in departure_positions]
    product = reduce(lambda a, b: a * b, departure_values, 1)
    print(product)


if __name__ == '__main__':
    main()

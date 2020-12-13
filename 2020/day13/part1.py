#!/usr/bin/env python

import sys
from heapq import heappush


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


def parse_lines(lines):
    arrival = int(lines[0])
    schedule = lines[1].split(',')
    buses = [int(x) for x in schedule if x != 'x']
    return arrival, buses


def find_next_bus(buses, arrival):
    heap = []
    for bus in buses:
        div = arrival // bus + 1
        heappush(heap, (bus * div, bus))

    return heap[0]


def main():
    lines = read_lines(sys.argv[1])
    arrival, buses = parse_lines(lines)
    next_bus_time, next_bus_id = find_next_bus(buses, arrival)
    print((next_bus_time - arrival) * next_bus_id)


if __name__ == '__main__':
    main()

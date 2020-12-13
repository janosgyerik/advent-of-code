#!/usr/bin/env python

import sys
from functools import reduce
from heapq import heappush


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


def parse_lines(lines):
    arrival = int(lines[0])
    schedule = lines[1].split(',')
    buses = [int(x) for x in schedule if x != 'x']
    return arrival, buses, schedule


def find_next_bus(buses, arrival):
    heap = []
    for bus in buses:
        div = arrival // bus + 1
        heappush(heap, (bus * div, bus))

    return heap[0]


def find_contest_timestamp(schedule):
    buses = [(int(x), offset) for offset, x in enumerate(schedule) if x != 'x']
    buses = sorted(buses, key=lambda x: -x[0])
    first = buses[0][0]
    candidate = first - buses[0][1]

    increment = first
    while True:
        for bus, offset in buses:
            if (candidate + offset) % bus != 0:
                candidate += increment
                break
            elif increment % bus != 0:
                increment *= bus
        else:
            return candidate


def main():
    lines = read_lines(sys.argv[1])
    arrival, buses, schedule = parse_lines(lines)
    next_bus_time, next_bus_id = find_next_bus(buses, arrival)
    print((next_bus_time - arrival) * next_bus_id)
    print(find_contest_timestamp(schedule))


if __name__ == '__main__':
    main()

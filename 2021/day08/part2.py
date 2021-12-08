#!/usr/bin/env python
import re
import sys
from collections import namedtuple, Counter, deque, defaultdict
from itertools import product
from heapq import heappush, heappop, heapify
from functools import lru_cache


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


def lines_to_ints(lines):
    return [int(x) for x in lines[0].split(',')]


possibles_by_length = {
    2: (1, ),
    3: (7, ),
    4: (4, ),
    5: (2, 3, 5),
    6: (0, 6, 9),
    7: (8, ),
}


def normalized(segments):
    return set(segments)


def normalized_list(segments_list):
    return [normalized(s) for s in segments_list]


class Entry:
    def __init__(self, inputs, outputs):
        self.inputs = normalized_list(inputs)
        self.outputs = normalized_list(outputs)

    def count_outputs_of_lengths(self, targets):
        return sum(1 for x in self.outputs if len(x) in targets)

    def decode(self):
        '''
  0:      1:      2:      3:      4:
 aaaa    ....    aaaa    aaaa    ....
b    c  .    c  .    c  .    c  b    c
b    c  .    c  .    c  .    c  b    c
 ....    ....    dddd    dddd    dddd
e    f  .    f  e    .  .    f  .    f
e    f  .    f  e    .  .    f  .    f
 gggg    ....    gggg    gggg    ....

  5:      6:      7:      8:      9:
 aaaa    aaaa    aaaa    aaaa    aaaa
b    .  b    .  .    c  b    c  b    c
b    .  b    .  .    c  b    c  b    c
 dddd    dddd    ....    dddd    dddd
.    f  e    f  .    f  e    f  .    f
.    f  e    f  .    f  e    f  .    f
 gggg    gggg    ....    gggg    gggg

        1, 4, 7, 8
        8 is useless
        how to distinguish:
        3: must contain all segments of 1
        2: must contain precisely 2 segments of 4
        5: else

        how to distinguish:
        9: must contain all segments of 4
        0: must not contain all segments of 4 and contain all segments of 7
        6: else

        '''
        mapping = self.compute_mapping(self.inputs)
        return self.compute_output(mapping, self.outputs)

    def compute_mapping(self, segments_list):
        mapping = {}
        segments_by_length = defaultdict(list)
        for segments in segments_list:
            segments_by_length[len(segments)].append(segments)

        mapping[1] = segments_by_length[2][0]
        mapping[4] = segments_by_length[4][0]
        mapping[7] = segments_by_length[3][0]
        mapping[8] = segments_by_length[7][0]

        for segment in segments_by_length[6]:
            if contains_all(segment, mapping[4]):
                mapping[9] = segment
            elif contains_all(segment, mapping[7]):
                mapping[0] = segment
            else:
                mapping[6] = segment

        for segment in segments_by_length[5]:
            if contains_all(segment, mapping[1]):
                mapping[3] = segment
            elif contains_two(segment, mapping[4]):
                mapping[2] = segment
            else:
                mapping[5] = segment

        return mapping

    def compute_output(self, mapping, segments_list):
        num = 0
        for segments in segments_list:
            num *= 10
            num += map_to_digit(segments, mapping)
        return num


def map_to_digit(segments, mapping):
    for digit, segments2 in mapping.items():
        if segments == segments2:
            return digit


def contains_all(segment, other):
    for x in other:
        if x not in segment:
            return False

    return True


def contains_two(segment, other):
    count = 0
    for x in other:
        if x in segment:
            count += 1

    return count == 2


def parse_entries(lines):
    for line in lines:
        inputs, outputs = line.split(' | ')
        inputs = inputs.split()
        outputs = outputs.split()
        yield Entry(inputs, outputs)


def solve(lines):
    entries = parse_entries(lines)
    total = 0
    for entry in entries:
        total += entry.decode()

    return total


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines))


if __name__ == '__main__':
    main()

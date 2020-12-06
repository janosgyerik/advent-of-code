#!/usr/bin/env python3

import sys
from collections import Counter


def read_answers_by_groups():
    groups = []
    answers = []
    for line in sys.stdin.readlines():
        line = line.rstrip()
        if not line:
            groups.append(answers.copy())
            answers.clear()
        else:
            answers.append(line)

    if answers:
        groups.append(answers)
            
    return groups


def count_unique_letters(answers):
    return sum(len(set(''.join(group))) for group in answers)


def count_common_answers(group):
    counts = Counter()
    for answer in group:
        counts.update(Counter(answer))
    return sum(1 for v in counts.values() if v == len(group))


def count_common_letters(answers):
    return sum(count_common_answers(group) for group in answers)


def main():
    answers = read_answers_by_groups()
    print(count_unique_letters(answers))
    print(count_common_letters(answers))


if __name__ == '__main__':
    main()

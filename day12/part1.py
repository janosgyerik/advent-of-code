#!/usr/bin/env python

import sys


def parse_rules(lines):
    rules = set()
    for line in lines:
        line = line.rstrip()
        if line[-1] != '#':
            continue
        pattern, _ = line.split(' => ')
        rules.add(pattern)
    return rules

def padded(start, s):
    '''
    >>> padded(0, '#')
    (-3, '...#...')
    >>> padded(-4, '#')
    (-7, '...#...')
    >>> padded(0, '##')
    (-3, '...##...')
    >>> padded(0, '..#..')
    (-1, '...#...')
    '''
    index = s.index('#')
    lpadding = max(0, 3 - index)
    rindex = s.rindex('#')
    rpadding = max(0, 3 - (len(s) - 1 - rindex))
    return start - lpadding, '.' * lpadding + s + '.' * rpadding

def next_gen(rules, pots):
    next_pots = ['.'] * len(pots)
    for i in range(2, len(pots) - 2):
        pattern = pots[i-2:i+3]
        if pattern in rules:
            next_pots[i] = '#'
    return ''.join(next_pots)

def sum_pots(start, pots):
    '''
    >>> sum_pots(0, '')
    0
    >>> sum_pots(0, '.#.#.')
    4
    >>> sum_pots(-3, '.#.#.')
    -2
    '''
    return sum(start + i for i in range(len(pots)) if pots[i] == '#')

def main():
    pots = sys.stdin.readline().split(': ')[1].strip()
    rules = parse_rules(sys.stdin.readlines()[1:])
    start, pots = padded(0, pots)
    prev = sum_pots(start, pots)
    for i in range(5000):
        start, pots = padded(start, pots)
        pots = next_gen(rules, pots)
        current = sum_pots(start, pots)
        if i % 1000 == 0:
            print(i, current, current - prev)
        prev = current

    print(sum_pots(start, pots))

if __name__ == '__main__':
    main()

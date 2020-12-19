#!/usr/bin/env python

import sys
import re


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


def parse_rule(line):
    key, rest = line.split(': ')
    key = int(key)

    if '"' in rest:
        return key, rest[1]

    refs = rest.split(' | ')
    return key, [[int(x) for x in part.split(' ')] for part in refs]


def parse_lines(lines):
    rules = {}
    index = 0
    for index, line in enumerate(lines):
        if not line:
            break

        key, rule = parse_rule(line)
        rules[key] = rule

    messages = lines[index+1:]
    return rules, messages


def build_regex(rule, rules):
    r = rules[rule]
    if type(r) is str:
        return r

    if type(r) is int:
        raise ValueError('Useless indirection?')

    if rule == 8:
        return f"({build_regex(42, rules)})+"

    if rule == 11:
        # 42 31 | 42 11 31
        # 42{n} 31{n}
        base = ''
        sb = []
        # since longest input line is 88, we might need 44 -> terminates in 12s
        # based on trial and error, 5 was good enough for my input -> terminates in < 1s
        for _ in range(5):
            base = build_regex(42, rules) + base + build_regex(31, rules)
            sb.append(base)
        return f"({'|'.join(f'({sub})' for sub in sb)})"

    sb = []
    if len(r) == 1:
        for child in r[0]:
            sb.append(build_regex(child, rules))

    else:
        sb.append('(')
        for child in r[0]:
            sb.append(build_regex(child, rules))
        sb.append('|')
        for child in r[1]:
            sb.append(build_regex(child, rules))
        sb.append(')')

    return ''.join(sb)


def matches(regex, m):
    return regex.fullmatch(m) is not None


def main():
    lines = read_lines(sys.argv[1])
    rules, messages = parse_lines(lines)
    # print(rules)
    regex = build_regex(0, rules)
    # print(regex)
    r = re.compile(regex)
    print(sum(1 for m in messages if matches(r, m)))


if __name__ == '__main__':
    main()

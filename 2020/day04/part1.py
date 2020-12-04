#!/usr/bin/env python3

import sys


def read_passports():
    passports = []
    passport = {}
    for line in sys.stdin.readlines():
        line = line.rstrip()
        if not line:
            passports.append(passport)
            passport = {}
        else:
            for kv in line.split(' '):
                k, v = kv.split(':')
                passport[k] = v

    if passport:
        passports.append(passport)
            
    return passports


def is_valid(passport):
    return len(passport) == 8 or len(passport) == 7 and 'cid' not in passport


def count_valid_passports(passports):
    return sum(1 for p in passports if is_valid(p))


def main():
    passports = read_passports()
    print(count_valid_passports(passports))


if __name__ == '__main__':
    main()

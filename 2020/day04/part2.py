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
    if not (len(passport) == 8 or len(passport) == 7 and 'cid' not in passport):
        return False

    if not '1920' <= passport['byr'] <= '2002':
        return False

    if not '2010' <= passport['iyr'] <= '2020':
        return False

    if not '2020' <= passport['eyr'] <= '2030':
        return False

    if passport['hgt'].endswith('in'):
        if not 59 <= int(passport['hgt'][:-2]) <= 76:
            return False

    elif passport['hgt'].endswith('cm'):
        if not 150 <= int(passport['hgt'][:-2]) <= 193:
            return False

    else:
        return False

    if len(passport['hcl']) != 7 or passport['hcl'][0] != '#':
        return False

    for c in passport['hcl'][1:]:
        if c not in '0123456789abcdef':
            return False

    if passport['ecl'] not in set('amb blu brn gry grn hzl oth'.split(' ')):
        return False

    if len(passport['pid']) != 9:
        return False

    for c in passport['pid']:
        if not '0' <= c <= '9':
            return False

    return True


def count_valid_passports(passports):
    return sum(1 for p in passports if is_valid(p))


def main():
    passports = read_passports()
    print(count_valid_passports(passports))


if __name__ == '__main__':
    main()

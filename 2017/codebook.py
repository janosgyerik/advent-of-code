#!/usr/bin/env python

import argparse


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


def solve(solver):
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    lines = read_lines(args.path)
    print(solver(lines))


def parse_ints(line):
    return [int(x) for x in line.split()]


def lines_to_ints(lines):
    return [int(line) for line in lines]

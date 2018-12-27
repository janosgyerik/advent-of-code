#!/usr/bin/env bash

cd "$(dirname "$0")"

for input in *.txt; do
    python ../part1.py < "$input"
done > actual.out

diff expected.out actual.out

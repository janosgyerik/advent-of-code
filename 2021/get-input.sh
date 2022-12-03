#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"
. config.sh

year=$(basename "$PWD")

input_file=tmp/input.txt

download_input() {
    local day input_url
    day=$1

    input_url=https://adventofcode.com/$year/day/$day/input
    curl -sb "session=$session" "$input_url" | tee "$input_file"
}

if [ $# = 0 ]; then
    day=$(date "+%d")
    day=${day#0}
else
    day=$1
fi

download_input "$day"

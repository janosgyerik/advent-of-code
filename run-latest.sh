#!/usr/bin/env bash

set -euo pipefail

year=$(basename "$PWD")
[[ $year == 20[1-9][0-9] ]] || {
    echo "Expected the directory name in $PWD to be a valid year, got: $year"
    exit 1
}

prog=$(command ls ./day??-part?.py | tail -n 1)

if [ $# = 0 ]; then
    set -- tmp/input.txt
fi

"$prog" "$@"

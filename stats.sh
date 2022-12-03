#!/usr/bin/env bash

set -euo pipefail

year=$(basename "$PWD")
[[ $year == 20[1-9][0-9] ]] || {
    echo "Expected the directory name in $PWD to be a valid year, got: $year"
    exit 1
}

. ../config.sh

stats_url="https://adventofcode.com/$year/leaderboard/private/view/$user.json"
stats_json=tmp/stats.json

download_stats() {
    curl -sb "session=$session" "$stats_url" | tee "$stats_json"
}

is_recently_downloaded() {
    find "$stats_json" -newerct '1 minute ago' | grep -q .
}

is_recently_downloaded || download_stats

python ../stats.py "$stats_json"

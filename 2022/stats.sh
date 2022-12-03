#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"
. config.sh

year=$(basename "$PWD")

stats_url="https://adventofcode.com/$year/leaderboard/private/view/$user.json"
stats_json=tmp/stats.json

download_stats() {
    curl -sb "session=$session" "$stats_url" | tee "$stats_json"
}

is_recently_downloaded() {
    find "$stats_json" -newerct '1 minute ago' | grep -q .
}

is_recently_downloaded || download_stats

./stats.py "$stats_json"

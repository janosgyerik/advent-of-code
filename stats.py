#!/usr/bin/env python
#
# download from: https://adventofcode.com/2021/leaderboard/private/view/631740.json
#
import json
import sys
from collections import defaultdict
from datetime import datetime

TOP = 5


def load_raw_json(path):
    with open(path) as fh:
        return json.load(fh)


def build_stats(raw_json):
    diffs = defaultdict(list)
    times = defaultdict(list)

    for member in raw_json['members'].values():
        for day, details in member['completion_day_level'].items():
            if not details:
                continue

            day = int(day)
            name = member['name']
            star_times = [int(details[x]['get_star_ts']) for x in '12' if x in details]

            times[day].append((star_times[0], '1', name))

            if len(star_times) == 2:
                diffs[day].append((star_times[1] - star_times[0], name))
                times[day].append((star_times[1], '2', name))

    def sorted_values(d):
        return {k: sorted(v) for k, v in d.items()}

    return sorted_values(diffs), sorted_values(times)


def print_heading(text):
    print(text)
    print('-' * len(text))


def format_time_delta(seconds):
    h = seconds // 3600
    m = (seconds // 60) % 60
    s = seconds % 60

    if h > 99:
        return 'LL:LL:LL'

    return f"{h:02d}:{m:02d}:{s:02d}"


def format_time(t):
    dt = datetime.fromtimestamp(t)
    return datetime.strftime(dt, '%Y-%m-%d %H:%M:%S')


def print_stats(diffs, times):
    for day in range(1, 26):
        if day not in times:
            continue
        print_heading(f'Day {day}: Top {TOP*2} submissions')
        rank = 1
        for t, part, name in times[day][:TOP*2]:
            print(f"{rank:2}. {format_time(t)} part {part} {name}")
            rank += 1
        print()

        print_heading(f'Day {day}: Fastest {TOP} for 2nd')
        rank = 1
        for dt, name in diffs[day][:TOP]:
            print(f"{rank}. {format_time_delta(dt)} {name}")
            rank += 1
        print()


def print_average_speed(diffs):
    ranks = defaultdict(list)
    for day in range(1, 26):
        if day not in diffs:
            continue
        rank = 1
        for dt, name in diffs[day]:
            ranks[name].append(rank)
            rank += 1

    rank_and_name = sorted((sum(r) / len(r), name) for name, r in ranks.items())
    print_heading('Average rank for speed for 2nd')
    for rank, name in rank_and_name[:TOP]:
        print(f"{rank:5.2f} {name}")


def main():
    path = sys.argv[1]
    raw_json = load_raw_json(path)
    diffs, times = build_stats(raw_json)
    print_stats(diffs, times)
    print_average_speed(diffs)


if __name__ == '__main__':
    main()

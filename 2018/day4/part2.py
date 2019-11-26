#!/usr/bin/env python

import sys, re
from collections import Counter
from itertools import chain

lines = sorted(sys.stdin.readlines())
guard_sleeps = {}
for line in lines:
    line = line.rstrip()
    if line.endswith('begins shift'):
        id_str = re.findall(r'\d{2}:\d{2}.*#(\d+)', line)[0]
        id_ = int(id_str)
        if id_ not in guard_sleeps:
            guard_sleeps[id_] = []
        continue

    time_str = re.findall(r'\d{2}:(\d{2})', line)[0]
    time = int(time_str)
    if line.endswith('falls asleep'):
        fell_asleep = time
        continue

    guard_sleeps[id_].append([fell_asleep, time])


sleepiest_minutes = [(id_, Counter(chain.from_iterable([list(range(s, w))
    for s, w in sleeps])).most_common()[0])
    for id_, sleeps in guard_sleeps.items() if sleeps]
sleepiest_id, (minute, _) = max(sleepiest_minutes, key=lambda e: e[1][1])
print(sleepiest_id * minute)

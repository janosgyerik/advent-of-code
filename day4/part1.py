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


sleepiest, sleeps = max(guard_sleeps.items(), key=lambda e: sum([w - s for s, w in e[1]]))
counter = Counter(chain.from_iterable([list(range(s, w)) for s, w in sleeps]))
print(counter.most_common()[0][0] * sleepiest)

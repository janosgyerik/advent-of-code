from collections import Counter
import sys

twice = 0
thrice = 0

for line in sys.stdin.readlines():
    c = Counter(line)
    s = set(c.values())
    if 2 in s:
        twice += 1
    if 3 in s:
        thrice += 1

print(twice * thrice)

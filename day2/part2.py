from collections import Counter
import sys

lines = list(sys.stdin.readlines())

for pos in range(len(lines[0])):
    chopped = [line[:pos] + line[pos+1:] for line in lines]
    c = Counter(chopped)
    for k, v in c.items():
        if v == 2:
            print(k)
            sys.exit(0)

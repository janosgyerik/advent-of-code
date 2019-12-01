#!/usr/bin/env awk -f

{
    t = $1
    while (1) {
        t = int(t / 3) - 2
        if (t <= 0) break
        s += t
    }
}

END {
    print s
}

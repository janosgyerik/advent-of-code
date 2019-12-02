#!/usr/bin/env awk -F, -f

{
    for (i = 1; i <= NF; i++) {
        mem[i-1] = $i
    }

    mem[1] = 12
    mem[2] = 2

    for (i = 0; i < NF; i += 4) {
        op = mem[i]
        s1 = mem[i+1]
        s2 = mem[i+2]
        t = mem[i+3]
        if (op == 1) mem[t] = mem[s1] + mem[s2]
        else if (op == 2) mem[t] = mem[s1] * mem[s2]
        else break
    }
}

END {
    print mem[0]
}

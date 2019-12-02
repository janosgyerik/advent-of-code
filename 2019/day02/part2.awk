#!/usr/bin/env awk -F, -f

{
    for (i = 1; i <= NF; i++) {
        mem[i-1] = $i
        backup[i-1] = $i
    }

    target = 19690720

    for (noun = 0; noun < 100; noun++) {
        for (verb = 0; verb < 100; verb++) {
            for (i = 0; i < NF; i++) {
                mem[i] = backup[i]
            }

            mem[1] = noun
            mem[2] = verb

            for (i = 0; i < NF; i += 4) {
                op = mem[i]
                s1 = mem[i+1]
                s2 = mem[i+2]
                t = mem[i+3]
                if (op == 1) mem[t] = mem[s1] + mem[s2]
                else if (op == 2) mem[t] = mem[s1] * mem[s2]
                else break
            }

            if (mem[0] == target) exit;
        }
    }
}

END {
    print 100 * noun + verb
}

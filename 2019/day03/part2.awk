#!/usr/bin/env awk -F, -f

{
    x = y = 0
    closest_dist = 4503599627370496
    total_steps = 0

    for (i = 1; i <= NF; i++) {
        desc = $i
        direction = substr(desc, 1, 1)
        steps = int(substr(desc, 2, length(desc)))

        if (direction == "U") {
            dx = 0
            dy = 1
        } else if (direction == "D") {
            dx = 0
            dy = -1
        } else if (direction == "L") {
            dx = -1
            dy = 0
        } else if (direction == "R") {
            dx = 1
            dy = 0
        }

        for (j = 0; j < steps; j++) {
            x += dx
            y += dy
            m[x,y]++

            total_steps++
            if (s[NR,x,y] == 0) s[NR,x,y] = total_steps

            if (m[x,y] > 1 && NR > 1 && s[1,x,y] > 0) {
                dist = s[1,x,y] + s[2,x,y]
                if (dist < closest_dist) closest_dist = dist
            }
        }
    }
}

END {
    print closest_dist
}

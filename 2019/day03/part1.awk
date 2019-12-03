#!/usr/bin/env awk -F, -f

{
    x = y = 0
    closest_dist = 4503599627370496

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
            if (m[x,y] > 1) {
                dist = x >= 0 ? x : -x;
                dist += y >= 0 ? y : -y;
                if (dist < closest_dist) closest_dist = dist
            }
        }
    }
}

END {
    print closest_dist
}

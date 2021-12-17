#!/usr/bin/env python

import os
import re
import shutil

solver_re = re.compile(r'day(?P<day>[012][0-9])-part(?P<part>[12]).py')
solver_format = 'day{day:02d}-part{part}.py'


def validate_day_and_part(day, part):
    if not (1 <= day <= 25 and 1 <= part <= 2):
        raise ValueError(f'Expected day in [1, 25] and part in [1, 2]; got day={day} part={part}')


def main():
    last_solver = ()
    for item in os.listdir():
        m = solver_re.match(item)
        if not m:
            continue

        day = int(m.group('day'))
        part = int(m.group('part'))
        validate_day_and_part(day, part)

        solver = day, part
        if last_solver < solver:
            last_solver = solver

    if last_solver == (25, 2):
        print('all done!')
    else:
        day, part = last_solver
        prev_solver_filename = solver_format.format(day=day, part=part)

        if part == 1:
            next_solver = day, 2
        else:
            next_solver = day + 1, 1

        day, part = next_solver

        next_solver_filename = solver_format.format(day=day, part=part)
        print(f'copying {prev_solver_filename} to {next_solver_filename}')

        shutil.copy(prev_solver_filename, next_solver_filename)


if __name__ == '__main__':
    main()

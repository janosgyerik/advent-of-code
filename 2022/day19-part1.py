#!/usr/bin/env python
import functools
import re
import sys
from collections import namedtuple, Counter, deque, defaultdict
from dataclasses import dataclass, field
from functools import lru_cache
from heapq import heappush, heappop, heapify
from itertools import product
from typing import Callable, List, Set, Tuple

import math

from utils.binary_search import binary_search
from utils import parsing
from utils import coordinates
from enum import Enum, auto


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


MAX_LENGTH = 14
MAX_LENGTH = 10


@dataclass(frozen=True)
class Blueprint:
    id_: int
    ore_cost: int
    clay_cost: int
    obsidian_cost_ore: int
    obsidian_cost_clay: int
    geode_cost_ore: int
    geode_cost_obsidian: int

    def want_more(self, r_ore, r_clay, r_obsidian):
        """
        >>> Blueprint(1, 4, 2, 3, 14, 2, 7).want_more(1, 0, 0)
        (True, True, True)

        >>> Blueprint(1, 4, 2, 3, 14, 2, 7).want_more(1, 0, 7)
        (True, False, False)

        >>> Blueprint(1, 4, 2, 3, 14, 2, 7).want_more(2, 0, 7)
        (False, False, False)

        >>> Blueprint(1, 4, 2, 3, 14, 2, 7).want_more(3, 14, 6)
        (False, False, True)

        >>> Blueprint(1, 4, 2, 3, 14, 2, 7).want_more(2, 14, 6)
        (True, False, True)

        >>> Blueprint(1, 4, 2, 3, 14, 2, 7).want_more(3, 13, 6)
        (False, True, True)

        """
        want_more_ore = r_ore < self.geode_cost_ore
        want_more_clay = False
        want_more_obsidian = r_obsidian < self.geode_cost_obsidian

        if want_more_obsidian:
            want_more_ore |= r_ore < self.obsidian_cost_ore
            want_more_clay = r_clay < self.obsidian_cost_clay

            if want_more_clay:
                want_more_ore |= r_ore < self.clay_cost

        return want_more_ore, want_more_clay, want_more_obsidian

    def compute_max_geodes(self, minutes):
        print(Blueprint(1, 1, 1, 1, 1, 1, 1).can_have_resources(Resource.ORE, 20, 10))
        return 0
        for count in range(1, 13):
            print(count, self.can_have_resources(Resource.GEODE, count, minutes))
        best = 0
        left = 1
        right = 172
        while left < right:
            mid = left + (right - left) // 2
            if self.can_have_resources(Resource.GEODE, mid, minutes):
                best = max(best, mid)
                left = mid + 1
            else:
                right = mid

        return best

    @lru_cache(maxsize=None)
    def can_have_resources(self, resource, count, minutes):
        """
        >>> Blueprint(0, 1, 1, 1, 1, 1, 1).can_have_resources(Resource.ORE, 1, 0)
        False

        >>> Blueprint(0, 1, 1, 1, 1, 1, 1).can_have_resources(Resource.ORE, 1, 1)
        True

        >>> Blueprint(0, 1, 1, 1, 1, 1, 1).can_have_resources(Resource.ORE, 2, 2)
        True

        >>> Blueprint(0, 1, 1, 1, 1, 1, 1).can_have_resources(Resource.ORE, 4, 4)
        True

        note: this is possible by not producing a robot in the round just before
        >>> Blueprint(0, 1, 1, 1, 1, 1, 1).can_have_resources(Resource.ORE, 5, 4)
        True

        >>> Blueprint(0, 1, 1, 1, 1, 1, 1).can_have_resources(Resource.ORE, 6, 4)
        False

        >>> Blueprint(0, 1, 1, 1, 1, 1, 1).can_have_resources(Resource.ORE, 7, 5)
        True

        >>> Blueprint(0, 1, 1, 1, 1, 1, 1).can_have_resources(Resource.ORE, 8, 5)
        True

        >>> Blueprint(0, 1, 1, 1, 1, 1, 1).can_have_resources(Resource.ORE, 9, 5)
        False

        >>> Blueprint(0, 1, 1, 1, 1, 1, 1).can_have_resources(Resource.ORE, 11, 6)
        True

        >>> Blueprint(0, 1, 1, 1, 1, 1, 1).can_have_resources(Resource.ORE, 12, 6)
        True

        >>> Blueprint(0, 1, 1, 1, 1, 1, 1).can_have_resources(Resource.ORE, 13, 6)
        False

        >>> Blueprint(0, 1, 1, 1, 1, 1, 1).can_have_resources(Resource.ORE, 16, 7)
        True

        >>> Blueprint(0, 1, 1, 1, 1, 1, 1).can_have_resources(Resource.ORE, 17, 7)
        True

        >>> Blueprint(0, 1, 1, 1, 1, 1, 1).can_have_resources(Resource.ORE, 18, 7)
        False

        >>> Blueprint(0, 1, 1, 1, 1, 1, 1).can_have_resources(Resource.ORE, 22, 8)
        True

        >>> Blueprint(0, 1, 1, 1, 1, 1, 1).can_have_resources(Resource.ORE, 23, 8)
        True

        >>> Blueprint(0, 1, 1, 1, 1, 1, 1).can_have_resources(Resource.ORE, 24, 8)
        False

        >>> Blueprint(0, 4, 2, 3, 14, 2, 7).can_have_resources(Resource.GEODE, 9, 24)
        True

        TODO: this should pass; the program seems to believe it can continue
        >>> Blueprint(0, 4, 2, 3, 14, 2, 7).can_have_resources(Resource.GEODE, 10, 24)
        False

        TODO: drop this redundant test
        >>> Blueprint(0, 4, 2, 3, 14, 2, 7).can_have_resources(Resource.GEODE, 18, 24)
        False

        >>> Blueprint(0, 2, 3, 3, 8, 3, 12).can_have_resources(Resource.GEODE, 12, 24)
        True

        TODO: this should pass; the program seems to believe it can continue
        >>> Blueprint(0, 2, 3, 3, 8, 3, 12).can_have_resources(Resource.GEODE, 13, 24)
        False

        TODO: drop this redundant test
        >>> Blueprint(0, 2, 3, 3, 8, 3, 12).can_have_resources(Resource.GEODE, 18, 24)
        False

        """
        assert count > 0
        assert minutes >= 0

        if minutes == 0:
            return False

        '''
        how can we have the required resources?
        they must have been produced.
        
        how could they have been produced?
        - by 1 robot, 1 per minute since count minutes, if feasible
            - or 1 per minute since count-1 minutes if there was 1 resource
            - or 1 per minute since count-2 minutes if there was 2 resource
            - ...
        - by 2 robots, 2 per minute some minutes ago, if feasible
        - by count robots, count in the last minute, if feasible
        '''

        for robots in range(1, count + 1):
            '''
            1 robot to produce N ->
                t-1: N-1 resources and 1 robot
                t-2: N-2 resources and 1 robot
                ...
                t-N: 1 robot
                
            2 robots to produce N ->
                t-1: N-2 resources and 2 robots
                t-2: N-4 resources and 2 robots
                ...
                t-d: 2 robots
            '''
            duration = math.ceil(count / robots)
            count2 = count

            for dt in range(1, duration + 1):
                minutes2 = minutes - dt
                if minutes2 < 0:
                    break

                count2 -= robots
                if count2 <= 0:
                    if self.can_have_robots(resource, robots, minutes2):
                        return True
                else:
                    if (self.can_have_robots(resource, robots, minutes2)
                            and self.can_have_resources(resource, count2, minutes2)):
                        return True

        return False

    @lru_cache(maxsize=None)
    def can_have_robots(self, resource, count, minutes):
        """
        >>> Blueprint(0, 1, 1, 1, 1, 1, 1).can_have_robots(Resource.ORE, 1, 0)
        True

        >>> Blueprint(0, 1, 1, 1, 1, 1, 1).can_have_robots(Resource.ORE, 2, 0)
        False

        >>> Blueprint(0, 1, 1, 1, 1, 1, 1).can_have_robots(Resource.ORE, 2, 1)
        True

        >>> Blueprint(0, 1, 1, 1, 1, 1, 1).can_have_robots(Resource.ORE, 3, 1)
        False

        >>> Blueprint(0, 1, 1, 1, 1, 1, 1).can_have_robots(Resource.ORE, 3, 2)
        True
        """
        assert count > 0
        assert minutes >= 0

        if minutes == 0:
            return resource == Resource.ORE and count == 1

        '''
        how can we have the required robots?
        they must have been produced.

        how could they have been produced?
        - we had the count - 1 in the previous round, and enough resources to make one
        '''

        if count == 1:
            if resource == Resource.ORE:
                return True

            if resource == Resource.CLAY:
                return self.can_have_resources(Resource.ORE, self.clay_cost, minutes - 1)

            if resource == Resource.OBSIDIAN:
                return (self.can_have_resources(Resource.ORE, self.obsidian_cost_ore, minutes - 1)
                        and self.can_have_resources(Resource.CLAY, self.obsidian_cost_clay, minutes - 1))

            if resource == Resource.GEODE:
                return (self.can_have_resources(Resource.ORE, self.geode_cost_ore, minutes - 1)
                        and self.can_have_resources(Resource.OBSIDIAN, self.geode_cost_obsidian, minutes - 1))

        if not self.can_have_robots(resource, count - 1, minutes - 1):
            return False

        if resource == Resource.ORE:
            return self.can_have_resources(Resource.ORE, self.ore_cost * count, minutes - 1)

        if resource == Resource.CLAY:
            return self.can_have_resources(Resource.ORE, self.clay_cost * count, minutes - 1)

        if resource == Resource.OBSIDIAN:
            return (self.can_have_resources(Resource.ORE, self.obsidian_cost_ore * count, minutes - 1)
                    and self.can_have_resources(Resource.CLAY, self.obsidian_cost_clay * count, minutes - 1))

        if resource == Resource.GEODE:
            return (self.can_have_resources(Resource.ORE, self.geode_cost_ore * count, minutes - 1)
                    and self.can_have_resources(Resource.OBSIDIAN, self.geode_cost_obsidian * count, minutes - 1))

        return False


class Resource(Enum):
    ORE = auto()
    CLAY = auto()
    OBSIDIAN = auto()
    GEODE = auto()


class Sequence:
    def __init__(self, code, length):
        self.code = code
        self.length = length

    def candidates(self):
        if self.length == MAX_LENGTH:
            return

        code = self.code
        digit = code % 10
        for prev in reversed(range(digit + 1)):
            yield Sequence(code * 10 + prev, self.length + 1)

        m = 10
        suffix = digit
        code //= 10
        while code:
            digit = code % 10
            for d in reversed(range(digit + 1)):
                candidate = (code * 10 + d) * m + suffix
                yield Sequence(candidate, self.length + 1)

            suffix = digit * m + suffix
            code //= 10
            m *= 10


@dataclass
class RobotFactory:
    blueprint: Blueprint
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0
    ore_robot: int = 1
    clay_robot: int = 0
    obsidian_robot: int = 0
    geode_robot: int = 0

    def work(self, minutes):
        # Resource.CLAY,
        # Resource.CLAY,
        # Resource.CLAY,
        # Resource.OBSIDIAN,
        # Resource.CLAY,
        # Resource.OBSIDIAN,
        # Resource.GEODE,
        # Resource.GEODE,

        start = Sequence(321, 3)
        start_geodes = self.mine(minutes, start)

        seen = set()

        def dfs(seq, geodes):
            max_geodes = geodes

            for candidate in seq.candidates():
                if candidate.code in seen:
                    continue

                seen.add(candidate.code)
                candidate_geodes = self.mine(minutes, candidate)
                if geodes <= candidate_geodes:
                    max_geodes = max(max_geodes, dfs(candidate, candidate_geodes))

            return max_geodes

        return dfs(start, start_geodes)

        q = deque([(start, start_geodes)])
        seen = set()
        max_geodes = start_geodes

        while q:
            seq, geodes = q.popleft()
            for candidate in seq.candidates():
                if candidate.code in seen:
                    continue

                seen.add(candidate.code)
                candidate_geodes = self.mine(minutes, candidate)
                if geodes <= candidate_geodes:
                    q.append((candidate, candidate_geodes))

                    if max_geodes < candidate_geodes:
                        max_geodes = candidate_geodes
                        # 11121233
                        print(candidate.code, max_geodes)

        return max_geodes

    def mine(self, minutes, sequence, debug=False):
        self.ore = 0
        self.clay = 0
        self.obsidian = 0
        self.geode = 0
        self.ore_robot = 1
        self.clay_robot = 0
        self.obsidian_robot = 0
        self.geode_robot = 0

        m = [Resource.ORE, Resource.CLAY, Resource.OBSIDIAN, Resource.GEODE]

        def gen():
            code = sequence.code
            while code:
                yield code % 10
                code //= 10

        it = (m[x] for x in gen())
        target = next(it)

        for i in range(minutes):
            if self.can_build(target):
                self.build(target)
                self.discount(target)
                try:
                    target = next(it)
                except StopIteration:
                    target = None

            self.ore += self.ore_robot
            self.clay += self.clay_robot
            self.obsidian += self.obsidian_robot
            self.geode += self.geode_robot
            if debug:
                print(f"{i:>2}:", f"{self.ore:>3}", f"{self.clay:>3}", f"{self.obsidian:>3}", f"{self.geode:>3}", '--',
                      self.ore_robot, self.clay_robot, self.obsidian_robot, self.geode_robot)

        return self.geode

    def can_build(self, target):
        if target is None:
            return False

        bp = self.blueprint

        if target == Resource.ORE:
            return self.ore >= bp.ore_cost

        if target == Resource.CLAY:
            return self.ore >= bp.clay_cost

        if target == Resource.OBSIDIAN:
            return self.ore >= bp.obsidian_cost_ore and self.clay >= bp.obsidian_cost_clay

        if target == Resource.GEODE:
            return self.ore >= bp.geode_cost_ore and self.obsidian >= bp.geode_cost_obsidian

    def build(self, target):
        bp = self.blueprint
        if target == Resource.ORE:
            self.ore -= bp.ore_cost
            self.ore_robot += 1

        elif target == Resource.CLAY:
            self.ore -= bp.clay_cost
            self.clay_robot += 1

        elif target == Resource.OBSIDIAN:
            self.ore -= bp.obsidian_cost_ore
            self.clay -= bp.obsidian_cost_clay
            self.obsidian_robot += 1

        elif target == Resource.GEODE:
            self.ore -= bp.geode_cost_ore
            self.obsidian -= bp.geode_cost_obsidian
            self.geode_robot += 1

    def discount(self, target):
        if target == Resource.ORE:
            self.ore -= 1
        elif target == Resource.CLAY:
            self.clay -= 1
        elif target == Resource.OBSIDIAN:
            self.obsidian -= 1
        elif target == Resource.GEODE:
            self.geode -= 1


@dataclass
class Blueprints:
    blueprints: List[Blueprint]

    def compute_total_quality(self, minutes):
        count = 0

        for bp in self.blueprints:
            factory = RobotFactory(bp)
            max_geodes = bp.compute_max_geodes(minutes)
            count0 = max_geodes * bp.id_
            xaa = 'x' + chr(ord('a') + (bp.id_ - 1) // 26) + chr(ord('a') + (bp.id_ - 1) % 26)
            print(f"{xaa}: {bp.id_} * {max_geodes} = {count0}")
            count += count0

        return count


def parse_blueprint(line):
    re_blueprint = re.compile(
        r'Blueprint (\d+): '
        r'Each ore robot costs (\d+) ore. '
        r'Each clay robot costs (\d+) ore. '
        r'Each obsidian robot costs (\d+) ore and (\d+) clay. '
        r'Each geode robot costs (\d+) ore and (\d+) obsidian.')

    args = [int(x) for x in re_blueprint.match(line).groups()]
    return Blueprint(*args)


def parse_blueprints(lines):
    blueprints = []
    for line in lines:
        blueprint = parse_blueprint(line)
        blueprints.append(blueprint)

    return Blueprints(blueprints)


def solve(lines, minutes, *args):
    minutes = int(minutes)
    blueprints = parse_blueprints(lines)
    if args:
        seq_spec = args[0]
        seq = Sequence(int(seq_spec), len(seq_spec))
        bp = blueprints.blueprints[0]
        print(bp)
        factory = RobotFactory(bp)
        max_geodes = factory.mine(minutes, seq, debug=True)
        print("max=", max_geodes, seq_spec)
        return

    return blueprints.compute_total_quality(minutes)


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines, *(sys.argv[2:])))


if __name__ == '__main__':
    main()

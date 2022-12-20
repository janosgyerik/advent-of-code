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

from utils.binary_search import binary_search
from utils import parsing
from utils import coordinates
from enum import Enum, auto


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


MAX_LENGTH = 14


@dataclass
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
        bp = self.blueprint
        match target:
            case None:
                return False
            case Resource.ORE:
                return self.ore >= bp.ore_cost
            case Resource.CLAY:
                return self.ore >= bp.clay_cost
            case Resource.OBSIDIAN:
                return self.ore >= bp.obsidian_cost_ore and self.clay >= bp.obsidian_cost_clay
            case Resource.GEODE:
                return self.ore >= bp.geode_cost_ore and self.obsidian >= bp.geode_cost_obsidian

    def build(self, target):
        bp = self.blueprint
        match target:
            case Resource.ORE:
                self.ore -= bp.ore_cost
                self.ore_robot += 1
            case Resource.CLAY:
                self.ore -= bp.clay_cost
                self.clay_robot += 1
            case Resource.OBSIDIAN:
                self.ore -= bp.obsidian_cost_ore
                self.clay -= bp.obsidian_cost_clay
                self.obsidian_robot += 1
            case Resource.GEODE:
                self.ore -= bp.geode_cost_ore
                self.obsidian -= bp.geode_cost_obsidian
                self.geode_robot += 1

    def discount(self, target):
        match target:
            case Resource.ORE:
                self.ore -= 1
            case Resource.CLAY:
                self.clay -= 1
            case Resource.OBSIDIAN:
                self.obsidian -= 1
            case Resource.GEODE:
                self.geode -= 1


@dataclass
class Blueprints:
    blueprints: List[Blueprint]

    def compute_total_quality(self, minutes):
        count = 0

        for bp in self.blueprints:
            factory = RobotFactory(bp)
            max_geodes = factory.work(minutes)
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

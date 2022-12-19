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


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


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
        bp = self.blueprint

        resources0 = (0, 0, 0, 0)
        robots0 = (1, 0, 0, 0)

        q = deque([(1, resources0, robots0)])
        max_geodes = 0

        while q:
            # print(q[0])
            m, res, robs = q.popleft()
            ore, clay, obsidian, geode = res
            r_ore, r_clay, r_obsidian, r_geode = robs

            # if geode == 1:
            #     print(m, res, robs)
            if geode > max_geodes:
                print(m, res, robs)
                max_geodes = geode
                self.ore, self.clay, self.obsidian, self.geode = res

            if m == minutes:
                break

            # want_more_ore, want_more_clay, want_more_obsidian = bp.want_more(r_ore, r_clay, r_obsidian)
            want_more_ore = r_ore < bp.geode_cost_ore
            want_more_clay = False
            want_more_obsidian = r_obsidian < bp.geode_cost_obsidian

            if want_more_obsidian:
                want_more_ore |= r_ore < bp.obsidian_cost_ore
                want_more_clay = r_clay < bp.obsidian_cost_clay

                if want_more_clay:
                    want_more_ore |= r_ore < bp.clay_cost

            if ore >= bp.geode_cost_ore and obsidian >= bp.geode_cost_obsidian:
                robots2 = r_ore, r_clay, r_obsidian, r_geode + 1
                res3 = ore + r_ore - bp.geode_cost_ore, clay + r_clay, obsidian + r_obsidian - bp.geode_cost_obsidian, geode + r_geode
                q.append((m + 1, res3, robots2))

                # greedy
                ore -= bp.geode_cost_ore
                obsidian -= bp.geode_cost_obsidian

            if want_more_obsidian and ore >= bp.obsidian_cost_ore and clay >= bp.obsidian_cost_clay:
                robots2 = r_ore, r_clay, r_obsidian + 1, r_geode
                res3 = ore + r_ore - bp.obsidian_cost_ore, clay + r_clay - bp.obsidian_cost_clay, obsidian + r_obsidian, geode + r_geode
                q.append((m + 1, res3, robots2))

                # greedy
                ore -= bp.obsidian_cost_ore
                clay -= bp.obsidian_cost_clay

            if want_more_clay and ore >= bp.clay_cost:
                robots2 = r_ore, r_clay + 1, r_obsidian, r_geode
                res3 = ore + r_ore - bp.clay_cost, clay + r_clay, obsidian + r_obsidian, geode + r_geode
                q.append((m + 1, res3, robots2))

                # greedy -> fast but incorrect result
                # ore -= bp.clay_cost

            if want_more_ore and ore >= bp.ore_cost:
                robots2 = r_ore + 1, r_clay, r_obsidian, r_geode
                res3 = ore + r_ore - bp.ore_cost, clay + r_clay, obsidian + r_obsidian, geode + r_geode
                q.append((m + 1, res3, robots2))

            res2 = ore + r_ore, clay + r_clay, obsidian + r_obsidian, geode + r_geode
            q.append((m + 1, res2, robs))


@dataclass
class Blueprints:
    blueprints: List[Blueprint]

    def compute_total_quality(self, minutes):
        count = 0

        for bp in self.blueprints:
            factory = RobotFactory(bp)
            factory.work(minutes)
            count += factory.geode * bp.id_

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
    return blueprints.compute_total_quality(minutes)


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines, *(sys.argv[2:])))


if __name__ == '__main__':
    main()

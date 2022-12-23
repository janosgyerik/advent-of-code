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


@dataclass()
class Blueprint:
    id_: int
    ore_cost: int
    clay_cost: int
    obsidian_cost_ore: int
    obsidian_cost_clay: int
    geode_cost_ore: int
    geode_cost_obsidian: int

    ore_robot_limit: int = field(init=False)
    clay_robot_limit: int = field(init=False)
    obsidian_robot_limit: int = field(init=False)

    def __post_init__(self):
        self.ore_robot_limit = max(self.ore_cost, self.clay_cost, self.obsidian_cost_ore, self.geode_cost_ore)
        self.clay_robot_limit = self.obsidian_cost_clay
        self.obsidian_robot_limit = self.geode_cost_obsidian


class Resource(Enum):
    ORE = auto()
    CLAY = auto()
    OBSIDIAN = auto()
    GEODE = auto()


RESOURCES = Resource.ORE, Resource.CLAY, Resource.OBSIDIAN, Resource.GEODE


@dataclass
class RobotFactory:
    blueprint: Blueprint


@dataclass(frozen=True)
class State:
    resources: Tuple = (0, 0, 0, 0)
    robots: Tuple = (1, 0, 0, 0)

    def choices(self, blueprint):
        if not self.robots[1] and self.resources[0] >= blueprint.ore_cost and self.resources[0] >= blueprint.clay_cost:
            pass
        elif (not self.robots[2]
              and self.resources[0] >= blueprint.ore_cost
              and self.resources[0] >= blueprint.clay_cost
              and self.resources[0] >= blueprint.obsidian_cost_ore
              and self.resources[0] >= blueprint.obsidian_cost_clay):
            pass
        elif (not self.robots[3]
              and self.resources[0] >= blueprint.ore_cost
              and self.resources[0] >= blueprint.clay_cost
              and self.resources[0] >= blueprint.obsidian_cost_ore
              and self.resources[0] >= blueprint.obsidian_cost_clay
              and self.resources[0] >= blueprint.geode_cost_ore
              and self.resources[0] >= blueprint.geode_cost_obsidian):
            pass
        else:
            yield State(tuple(x + r for x, r in zip(self.resources, self.robots)), self.robots)

        if self.robots[0] < blueprint.ore_robot_limit and self.resources[0] >= blueprint.ore_cost:
            yield State(self.used(0, blueprint.ore_cost), self.built(0))

        if self.robots[1] < blueprint.clay_robot_limit and self.resources[0] >= blueprint.clay_cost:
            yield State(self.used(0, blueprint.clay_cost), self.built(1))

        if (self.robots[2] < blueprint.obsidian_robot_limit
                and self.resources[0] >= blueprint.obsidian_cost_ore
                and self.resources[1] >= blueprint.obsidian_cost_clay):
            yield State(self.used2(blueprint.obsidian_cost_ore, 1, blueprint.obsidian_cost_clay), self.built(2))

        if self.resources[0] >= blueprint.geode_cost_ore and self.resources[2] >= blueprint.geode_cost_obsidian:
            yield State(self.used2(blueprint.geode_cost_ore, 2, blueprint.geode_cost_obsidian), self.built(3))

    def used(self, index, count):
        assert self.resources[index] >= count

        if index == 0:
            return (
                self.resources[0] - count + self.robots[0],
                self.resources[1] + self.robots[1],
                self.resources[2] + self.robots[2],
                self.resources[3] + self.robots[3],
            )

        if index == 1:
            return (
                self.resources[0] + self.robots[0],
                self.resources[1] - count + self.robots[1],
                self.resources[2] + self.robots[2],
                self.resources[3] + self.robots[3],
            )

        raise ValueError('invalid index to use ore')

    def used2(self, count, index2, count2):
        assert self.resources[0] >= count
        assert self.resources[index2] >= count2

        if index2 == 1:
            return (
                self.resources[0] - count + self.robots[0],
                self.resources[1] - count2 + self.robots[1],
                self.resources[2] + self.robots[2],
                self.resources[3] + self.robots[3],
            )

        if index2 == 2:
            return (
                self.resources[0] - count + self.robots[0],
                self.resources[1] + self.robots[1],
                self.resources[2] - count2 + self.robots[2],
                self.resources[3] + self.robots[3],
            )

        raise ValueError(f'invalid index for 2nd resource: {index2}')

    def built(self, index):
        if index == 0:
            return self.robots[0] + 1, self.robots[1], self.robots[2], self.robots[3]
        if index == 1:
            return self.robots[0], self.robots[1] + 1, self.robots[2], self.robots[3]
        if index == 2:
            return self.robots[0], self.robots[1], self.robots[2] + 1, self.robots[3]
        if index == 3:
            return self.robots[0], self.robots[1], self.robots[2], self.robots[3] + 1

        raise ValueError('not implemented yet')

    @property
    def geodes_plus_robots(self):
        return self.resources[-1] + self.robots[-1]


def compute_max_geodes(blueprint, minutes):
    """
    We have a state machine, expressed by the collection of resources and robots.
    In each state:
    - resources are produced
    - we can do nothing or make robots

    To find the maximum geodes we can have, we explore reachable states in 24 steps.
    Some states are clearly inferior to others and should not be explored.
    """
    q = [State()]
    for minute in range(minutes - 1):
        print(minute, len(q))
        q2 = []
        for s in q:
            for s2 in s.choices(blueprint):
                q2.append(s2)

        # TODO filter q2, excluding poor choices
        q = q2

    max_geodes = 0
    for s in q:
        max_geodes = max(max_geodes, s.geodes_plus_robots)

    return max_geodes


@dataclass
class Blueprints:
    blueprints: List[Blueprint]

    def compute_total_quality(self, minutes):
        total = 0

        for bp in self.blueprints:
            max_geodes = compute_max_geodes(bp, minutes)
            count = max_geodes * bp.id_
            total += count

        return total


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

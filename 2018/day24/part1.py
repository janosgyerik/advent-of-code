#!/usr/bin/env python

import sys, re

re_base_spec = re.compile(r'(?P<units>\d+) units each with (?P<hp>\d+) hit points.* with an attack that does (?P<damage>\d+) (?P<dtype>\w+) damage at initiative (?P<initiative>\d+)')
re_weak_to = re.compile(r'weak to ([\w, ]+)')
re_immune_to = re.compile(r'immune to ([\w, ]+)')


class Group:
    counts = {}

    def __init__(self, team, line, units, hp, damage, dtype, initiative, weaknesses, immunities):
        self.team = team
        self.counts[team] = self.counts[team] + 1 if team in self.counts else 1
        self.name = f'{team} group {self.counts[team]}'
        self.line = line
        self.units = units
        self.hp = hp
        self.initiative = initiative
        self.damage = damage
        self.dtype = dtype
        self.weaknesses = weaknesses
        self.immunities = immunities

    def display(self):
        print(f'{self.line}\n{self.units} units each with {self.hp} hit points (weak to {self.weaknesses}; immune to {self.immunities}) with an attack that does {self.damage} {self.dtype} damage at initiative {self.initiative}')

    def effective_power(self):
        return self.units * self.damage

    def potential_damage(self, defender):
        if self.dtype in defender.immunities:
            return 0

        damage = self.effective_power()
        if self.dtype in defender.weaknesses:
            return 2 * damage

        return damage

    def receive_damage(self, damage):
        self.units = max(0, self.units - damage // self.hp)
        if not self.units:
            self.team.groups.remove(self)

    def __str__(self):
        return self.name


class Team:
    def __init__(self, name, groups):
        self.name = name
        self.groups = groups

    def display(self):
        for group in self.groups:
            group.display()
        print()

    def __str__(self):
        return self.name


def parse_teams(lines):
    teams = []
    groups = []
    for line in lines:
        line = line.rstrip()
        if line.endswith(':'):
            team = Team(line[:-1], groups)
            teams.append(team)
            continue

        if not line:
            groups = []
            continue

        groups.append(parse_group(team, line))

    return teams


def parse_group(team, line):
    m = re_base_spec.match(line)
    units = int(m.group('units'))
    hp = int(m.group('hp'))
    damage = int(m.group('damage'))
    dtype = m.group('dtype')
    initiative = int(m.group('initiative'))

    raw_weaknesses = re_weak_to.search(line)
    if raw_weaknesses:
        weaknesses = set(raw_weaknesses.group(1).split(', '))
    else:
        weaknesses = set()

    raw_immunities = re_immune_to.search(line)
    if raw_immunities:
        immunities = set(raw_immunities.group(1).split(', '))
    else:
        immunities = set()

    return Group(team, line, units, hp, damage, dtype, initiative, weaknesses, immunities)


class Combat:
    def __init__(self, teams):
        self.teams = teams

    def play_round(self):
        for attacker, defender in sorted(self.target_selection(), key=lambda t: t[0].initiative, reverse=True):
            if attacker.units:
                damage = attacker.potential_damage(defender)
                defender.receive_damage(damage)

    def target_selection(self):
        attackers = set(self.teams[0].groups + self.teams[1].groups)
        defenders = set(self.teams[0].groups + self.teams[1].groups)

        while attackers:
            attacker = self.next_attacker(attackers)
            attackers.remove(attacker)
            defender, damage = self.next_defender(attacker, defenders - set(attacker.team.groups))
            if defender and damage:
                defenders.remove(defender)
                yield attacker, defender

    def next_attacker(self, available):
        return max(available, key=lambda group: (group.effective_power(), group.initiative))

    def next_defender(self, attacker, available):
        if not available:
            return None, None
        defender = max(available, key=lambda defender: (attacker.potential_damage(defender), defender.effective_power(), defender.initiative))
        return defender, attacker.potential_damage(defender)

    def fight_to_death(self):
        rounds = 0
        while all([team.groups for team in self.teams]):
            rounds += 1
            self.play_round()
            for team in teams:
                team.display()

        winner = self.teams[0] if self.teams[0].groups else self.teams[1]
        print(f'ended after {rounds} rounds, winning team is {winner}')

    def compute_score(self):
        return sum([g.units for g in self.teams[0].groups + self.teams[1].groups])

if __name__ == '__main__':
    teams = parse_teams(sys.stdin.readlines())
    combat = Combat(teams)
    combat.fight_to_death()
    print(combat.compute_score())

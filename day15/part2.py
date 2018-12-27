#!/usr/bin/env python

import sys


class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Pos(self.x + other.x, self.y + other.y)

    def __hash__(self):
        return self.x * 13 + self.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)

    def __repr__(self):
        return self.__str__()


class Maze:
    WALL = '#'
    EMPTY = '.'
    ELF = 'E'
    GOBLIN = 'G'
    DIRECTIONS = Pos(0, -1), Pos(-1, 0), Pos(1, 0), Pos(0, 1)

    def __init__(self, lines):
        self.elves_attack = 3
        self.lines = lines
        self.reset()

    def reset(self):
        self.elves = []
        self.goblins = []
        self.grid = []
        self.cell_at = {}
        self.fighter_at = {}
        self.parse_grid(self.lines)
        self.elves_orig_count = len(self.elves)

    def all_elves_alive(self):
        return len(self.elves) == self.elves_orig_count

    def parse_grid(self, lines):
        for y, line in enumerate(lines):
            row = []
            for x, c in enumerate(line.rstrip()):
                pos = Pos(x, y)
                if c == self.ELF:
                    fighter = Fighter(self.ELF, self.GOBLIN, pos, self.elves_attack)
                    self.fighter_at[pos] = fighter
                    self.elves.append(fighter)
                elif c == self.GOBLIN:
                    fighter = Fighter(self.GOBLIN, self.ELF, pos, 3)
                    self.fighter_at[pos] = fighter
                    self.goblins.append(fighter)
                elif c == self.WALL or c == self.EMPTY:
                    pass
                else:
                    raise ValueError("Unknown tile type: " + c)

                self.cell_at[pos] = c
                row.append(c)

            self.grid.append(row)

    def has_dead_team(self):
        return not self.elves or not self.goblins

    def fighters(self):
        for fighter in sorted(self.elves + self.goblins, key=lambda f: (f.pos.y, f.pos.x)):
            if fighter.alive:
                yield fighter

    def is_valid(self, pos):
        return 0 <= pos.x and 0 <= pos.y and pos.x < len(self.grid[0]) and pos.y < len(self.grid)

    def find_adjacent_enemy(self, fighter):
        enemies = []
        for d in self.DIRECTIONS:
            pos = fighter.pos + d
            if self.is_valid(pos) and self.get_cell(pos) == fighter.target:
                enemies.append(self.get_fighter(pos))

        return min(enemies, key=lambda f: f.hp) if enemies else None

    def path_from_nearest_enemy(self, fighter):
        adjacent = self.find_adjacent_enemy(fighter)
        if adjacent:
            return []

        enemies = self.goblins if fighter.team == self.ELF else self.elves
        targets = set()
        for enemy in enemies:
            for d in self.DIRECTIONS:
                pos2 = enemy.pos + d
                if self.is_valid(pos2) and self.get_cell(pos2) == self.EMPTY:
                    targets.add(pos2)

        me = self.get_cell(fighter.pos)
        q = [fighter.pos]
        links = {}
        paths_list = []
        while q and not paths_list:
            for _ in range(len(q)):
                pos = q[0]
                q = q[1:]
                for d in self.DIRECTIONS:
                    pos2 = pos + d
                    if not self.is_valid(pos2) or pos2 in links:
                        continue

                    if pos2 in targets:
                        path = [pos2]
                        pos2 = pos
                        while self.get_cell(pos2) != me:
                            path.append(pos2)
                            pos2 = links[pos2]
                        paths_list.append(path)
                        continue

                    if self.get_cell(pos2) == self.EMPTY:
                        links[pos2] = pos
                        q.append(pos2)

        return min(paths_list, key=lambda p: (p[0].y, p[0].x)) if paths_list else None

    def move_toward(self, fighter, path_from_enemy):
        self.clear_fighter(fighter)
        fighter.pos = path_from_enemy[-1]
        self.set_fighter(fighter)

    def attack_weakest_adjacent(self, fighter):
        enemy = self.find_adjacent_enemy(fighter)
        if enemy:
            self.attack(fighter, enemy)

    def attack(self, fighter, target):
        if not target.alive:
            return

        target.hp -= fighter.attack
        if target.hp <= 0:
            if target in self.elves:
                self.elves.remove(target)
            else:
                self.goblins.remove(target)

            target.alive = False
            self.clear_fighter(target)

    def get_cell(self, pos):
        return self.cell_at[pos]

    def set_cell(self, pos, cell):
        self.grid[pos.y][pos.x] = cell
        self.cell_at[pos] = cell

    def clear_cell(self, pos):
        self.grid[pos.y][pos.x] = self.EMPTY
        self.cell_at[pos] = self.EMPTY

    def get_fighter(self, pos):
        return self.fighter_at[pos]

    def set_fighter(self, fighter):
        self.set_cell(fighter.pos, fighter.team)
        self.fighter_at[fighter.pos] = fighter

    def clear_fighter(self, fighter):
        self.clear_cell(fighter.pos)
        del self.fighter_at[fighter.pos]

    def display(self):
        for row in self.grid:
            print(''.join(row))
        print()
        
        for fighter in self.fighters():
            print(fighter)
        print()


class Fighter:
    def __init__(self, team, target, pos, attack):
        self.team = team
        self.target = target
        self.pos = pos
        self.attack = attack
        self.hp = 200
        self.alive = True

    def __str__(self):
        return '{}({}) @ {}'.format(self.team, self.hp, self.pos)


class Combat:
    def __init__(self, maze):
        self.maze = maze
        self.round = 0

    def play_round(self):
        self.round += 1
        for fighter in self.maze.fighters():
            if self.is_over():
                return True
            path_from_enemy = self.maze.path_from_nearest_enemy(fighter)
            if path_from_enemy:
                self.maze.move_toward(fighter, path_from_enemy)

            self.maze.attack_weakest_adjacent(fighter)

        return False

    def fight_to_death(self):
        self.round = 0
        while not self.play_round():
            pass

    def fight_to_first_elf_death_or_glory(self):
        self.round = 0
        while not self.play_round():
            if not self.maze.all_elves_alive():
                return

    def is_over(self):
        return self.maze.has_dead_team()

    def print_outcome(self):
        full_rounds = self.round - 1
        print('Combat ends after {} full rounds'.format(full_rounds))
        winner = 'Goblins' if self.maze.goblins else 'Elves'
        total_hp = sum(f.hp for f in self.maze.fighters())
        print('{} win with {} total hit points left'.format(winner, total_hp))
        print('Outcome: {} * {} = {}'.format(full_rounds, total_hp, full_rounds * total_hp))


class Simulator:
    def __init__(self, maze):
        self.maze = maze
        self.combat = Combat(maze)

    def bolster_elves_until_they_win_without_losses(self):
        while True:
            self.maze.elves_attack *= 2
            self.maze.reset()
            self.combat.fight_to_first_elf_death_or_glory()
            if self.maze.all_elves_alive():
                return

    def weaken_elves_until_they_incur_losses(self):
        while True:
            self.maze.elves_attack -= 1
            self.maze.reset()
            self.combat.fight_to_first_elf_death_or_glory()
            if not self.maze.all_elves_alive():
                return

    def compute_optimal_outcome(self):
        self.bolster_elves_until_they_win_without_losses()
        self.weaken_elves_until_they_incur_losses()
        self.maze.elves_attack += 1
        self.maze.reset()
        self.combat.fight_to_death()

    def compute_and_print_optimal_outcome(self):
        self.compute_optimal_outcome()
        self.combat.print_outcome()

if __name__ == '__main__':
    maze = Maze(sys.stdin.readlines())
    Simulator(maze).compute_and_print_optimal_outcome()

#!/usr/bin/env python
# fix full rounds count for sample.txt
# -> fix end condition: when a fighter finds no target because all enemy are dead

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
        self.elves = []
        self.goblins = []
        self.grid = []
        self.cell_at = {}
        self.fighter_at = {}
        self.parse_grid(lines)

    def parse_grid(self, lines):
        for y, line in enumerate(lines):
            row = []
            for x, c in enumerate(line.rstrip()):
                pos = Pos(x, y)
                if c == self.ELF:
                    fighter = Fighter(self.ELF, self.GOBLIN, pos)
                    self.fighter_at[pos] = fighter
                    self.elves.append(fighter)
                elif c == self.GOBLIN:
                    fighter = Fighter(self.GOBLIN, self.ELF, pos)
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

        me = self.get_cell(fighter.pos)
        q = [fighter.pos]
        links = {}
        while q:
            pos = q[0]
            q = q[1:]
            for d in self.DIRECTIONS:
                pos2 = pos + d
                if not self.is_valid(pos2) or pos2 in links:
                    continue

                if self.get_cell(pos2) == fighter.target:
                    path = [pos2]
                    pos2 = pos
                    while self.get_cell(pos2) != me:
                        path.append(pos2)
                        pos2 = links[pos2]
                    return path

                if self.get_cell(pos2) == self.EMPTY:
                    links[pos2] = pos
                    q.append(pos2)

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
    def __init__(self, team, target, pos):
        self.team = team
        self.target = target
        self.pos = pos
        self.hp = 200
        self.attack = 3
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

    def is_over(self):
        return self.maze.has_dead_team()

    def print_outcome(self):
        full_rounds = self.round - 1
        print('Combat ends after {} full rounds'.format(full_rounds))
        winner = 'Goblins' if self.maze.goblins else 'Elves'
        total_hp = sum(f.hp for f in self.maze.fighters())
        print('{} win with {} total hit points left'.format(winner, total_hp))
        print('Outcome: {} * {} = {}'.format(full_rounds, total_hp, full_rounds * total_hp))

if __name__ == '__main__':
    maze = Maze(sys.stdin.readlines())
    combat = Combat(maze)
    while not combat.play_round():
        maze.display()

    combat.print_outcome()

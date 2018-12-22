#!/usr/bin/env python

import sys
from collections import deque


class Graph:
    def __init__(self):
        self.carts = []
        self.lines = []

    def add_line(self, line):
        self.lines.append(list(line))

    def add_cart(self, cart):
        self.carts.append(cart)

    def move_carts(self):
        sorted_carts = sorted(self.carts, key=lambda c: (c.pos.y, c.pos.x))
        taken = set(cart.pos for cart in self.carts)
        for cart in sorted_carts:
            old_pos = cart.pos
            cart.pos += cart.direction

            if cart.pos in taken:
                return cart.pos

            taken.add(cart.pos)
            taken.remove(old_pos)

            if cart.direction == D_LEFT:
                if self.at(cart.pos) == '\\':
                    cart.direction = D_UP
                elif self.at(cart.pos) == '/':
                    cart.direction = D_DOWN
                elif self.at(cart.pos) == '+':
                    cart.turn()
                elif self.at(cart.pos) in '-|':
                    pass
                else:
                    raise ValueError('Unexpected position: ' + self.at(cart.pos))

            elif cart.direction == D_RIGHT:
                if self.at(cart.pos) == '\\':
                    cart.direction = D_DOWN
                elif self.at(cart.pos) == '/':
                    cart.direction = D_UP
                elif self.at(cart.pos) == '+':
                    cart.turn()
                elif self.at(cart.pos) in '-|':
                    pass
                else:
                    raise ValueError('Unexpected position: ' + self.at(cart.pos))

            elif cart.direction == D_UP:
                if self.at(cart.pos) == '\\':
                    cart.direction = D_LEFT
                elif self.at(cart.pos) == '/':
                    cart.direction = D_RIGHT
                elif self.at(cart.pos) == '+':
                    cart.turn()
                elif self.at(cart.pos) in '-|':
                    pass
                else:
                    raise ValueError('Unexpected position: ' + self.at(cart.pos))

            elif cart.direction == D_DOWN:
                if self.at(cart.pos) == '\\':
                    cart.direction = D_RIGHT
                elif self.at(cart.pos) == '/':
                    cart.direction = D_LEFT
                elif self.at(cart.pos) == '+':
                    cart.turn()
                elif self.at(cart.pos) in '-|':
                    pass
                else:
                    raise ValueError('Unexpected position: ' + self.at(cart.pos))

    def at(self, pos):
        return self.lines[pos.y][pos.x]


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


class Cart:
    def __init__(self, x, y, c):
        self.pos = Pos(x, y)
        self.direction = self.parse_direction(c)
        self.directions = deque([D_LEFT, Pos(0, 0), D_RIGHT])

    def parse_direction(self, c):
        if c == '<':
            return D_LEFT
        if c == '>':
            return D_RIGHT
        if c == 'v':
            return D_DOWN
        if c == '^':
            return D_UP
        raise ValueError('Unexpected direction: ' + c)

    def turn(self):
        if self.directions[0] == D_LEFT:
            if self.direction == D_LEFT:
                self.direction = D_DOWN
            elif self.direction == D_RIGHT:
                self.direction = D_UP
            elif self.direction == D_UP:
                self.direction = D_LEFT
            elif self.direction == D_DOWN:
                self.direction = D_RIGHT
            else:
                raise ValueError('Unexpected cart direction: ' + self.direction)

        elif self.directions[0] == D_RIGHT:
            if self.direction == D_LEFT:
                self.direction = D_UP
            elif self.direction == D_RIGHT:
                self.direction = D_DOWN
            elif self.direction == D_UP:
                self.direction = D_RIGHT
            elif self.direction == D_DOWN:
                self.direction = D_LEFT
            else:
                raise ValueError('Unexpected cart direction: ' + self.direction)

        self.directions.rotate(-1)

    def __str__(self):
        return '{} {} {}'.format(self.pos, self.direction, self.directions)

def parse_input():
    g = Graph()
    for y, line in enumerate(sys.stdin.readlines()):
        g.add_line(line.replace('v', '|').replace('^', '|').replace('<', '-').replace('>', '-'))
        for x, c in enumerate(line):
            if c in '<>v^':
                cart = Cart(x, y, c)
                g.add_cart(cart)
    return g

D_UP = Pos(0, -1)
D_DOWN = Pos(0, 1)
D_LEFT = Pos(-1, 0)
D_RIGHT = Pos(1, 0)

if __name__ == '__main__':
    g = parse_input()
    for i in range(1000):
        pos = g.move_carts()
        if pos:
            print(i, pos, g.lines[pos.y][pos.x])
            break

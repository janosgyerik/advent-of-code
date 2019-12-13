#!/usr/bin/env python3
import math
import sys


class Body:
    def __init__(self, x, y, z, vx=0, vy=0, vz=0):
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz

    def apply_velocity(self):
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz

    def apply_gravity(self, other):
        if self.x < other.x:
            self.vx += 1
            other.vx -= 1
        elif other.x < self.x:
            self.vx -= 1
            other.vx += 1

        if self.y < other.y:
            self.vy += 1
            other.vy -= 1
        elif other.y < self.y:
            self.vy -= 1
            other.vy += 1

        if self.z < other.z:
            self.vz += 1
            other.vz -= 1
        elif other.z < self.z:
            self.vz -= 1
            other.vz += 1

    def energy(self):
        return sum(abs(v) for v in (self.x, self.y, self.z)) * sum(abs(v) for v in (self.vx, self.vy, self.vz))

    def __str__(self):
        return f"pos=<x={self.x}, y={self.y}, z={self.z}>, vel=<x={self.vx}, y={self.vy}, z={self.vz}>"

    def __eq__(self, other):
        return (self.x == other.x and self.y == other.y and self.z == other.z
                and self.vx == other.vx and self.vy == other.vy and self.vz == other.vz)

    def copy(self):
        return Body(self.x, self.y, self.z, self.vx, self.vy, self.vz)

    def display(self):
        print(self)


class Simulation:
    def __init__(self, bodies):
        self.bodies = bodies

    def step(self):
        self.apply_gravity()
        self.apply_velocity()

    def apply_gravity(self):
        for i in range(len(self.bodies)):
            for j in range(i + 1, len(self.bodies)):
                self.bodies[i].apply_gravity(self.bodies[j])

    def apply_velocity(self):
        for b in self.bodies:
            b.apply_velocity()

    def energy(self):
        return sum(b.energy() for b in self.bodies)

    def display(self):
        for b in self.bodies:
            b.display()
        print()

    def copy(self):
        return Simulation([b.copy() for b in self.bodies])

    def __eq__(self, other):
        return all(self.bodies[i] == other.bodies[i] for i in range(len(self.bodies)))


def xyz(s):
    return [int(x[x.index('=') + 1:]) for x in s[:-1].split(', ')]


def cycle_length(orig, fun):
    i = 0
    sim = orig.copy()
    while True:
        sim.step()
        i += 1
        if fun(sim) == fun(orig):
            return i


def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


def main():
    bodies = [Body(*xyz(line.rstrip())) for line in sys.stdin.readlines()]
    sim = Simulation(bodies)
    a = cycle_length(sim, lambda s: [(b.x, b.vx) for b in s.bodies])
    b = cycle_length(sim, lambda s: [(b.y, b.vy) for b in s.bodies])
    c = cycle_length(sim, lambda s: [(b.z, b.vz) for b in s.bodies])
    print(a, b, c, lcm(a, lcm(b, c)))


if __name__ == '__main__':
    main()

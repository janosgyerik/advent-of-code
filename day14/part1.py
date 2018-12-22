#!/usr/bin/env python

import sys


class RecipeMachine:
    def __init__(self):
        self.leaderboard = [3, 7]
        self.elf1 = 0
        self.elf2 = 1

    def make(self):
        recipe = self.leaderboard[self.elf1] + self.leaderboard[self.elf2]
        self.leaderboard.extend([int(x) for x in str(recipe)])
        self.elf1 = self.next_index(self.elf1)
        self.elf2 = self.next_index(self.elf2)

    def next_index(self, index):
        '''
        >>> rm = RecipeMachine(); rm.make(); rm.leaderboard, rm.elf1, rm.elf2
        ([3, 7, 1, 0], 0, 1)
        >>> rm = RecipeMachine(); rm.make(); rm.make(); rm.leaderboard, rm.elf1, rm.elf2
        ([3, 7, 1, 0, 1, 0], 4, 3)
        >>> rm = RecipeMachine(); _ = [rm.make() for _ in range(3)]; rm.leaderboard, rm.elf1, rm.elf2
        ([3, 7, 1, 0, 1, 0, 1], 6, 4)
        >>> rm = RecipeMachine(); _ = [rm.make() for _ in range(4)]; rm.leaderboard, rm.elf1, rm.elf2
        ([3, 7, 1, 0, 1, 0, 1, 2], 0, 6)
        '''
        length = len(self.leaderboard)
        return (index + 1 + self.leaderboard[index]) % length

if __name__ == '__main__':
    length = int(sys.argv[1])
    rm = RecipeMachine()
    for _ in range(max(50, length)):
        rm.make()

    print(''.join(str(x) for x in rm.leaderboard[length:length+10]))

#!/usr/bin/env python
import re
import sys
from collections import namedtuple, Counter, deque, defaultdict
from itertools import product
from heapq import heappush, heappop, heapify
from functools import lru_cache


class Board:
    def __init__(self, grid):
        self.rows = grid

        cols = [[] for _ in range(5)]
        for i in range(5):
            for j in range(5):
                cols[j].append(grid[i][j])
        self.cols = cols

        unmarked = set()
        for row in grid:
            unmarked.update(row)

        self.unmarked = unmarked

    def mark(self, num):
        if num in self.unmarked:
            self.unmarked.remove(num)

    def is_winner(self, nums):
        return self._is_winner(nums, self.rows) or self._is_winner(nums, self.cols)

    def _is_winner(self, nums, arr):
        for row in arr:
            for x in row:
                if x not in nums:
                    break
            else:
                # print(row)
                # print(nums)
                return True

        return False


class Bingo:
    def __init__(self, nums, boards):
        self.ordered_nums = nums
        self.nums = set()
        self.boards = [Board(board) for board in boards]

    def play(self):
        for num in self.ordered_nums:
            self.nums.add(num)
            for board in self.boards:
                board.mark(num)
                if board.is_winner(self.nums):
                    s = sum(board.unmarked)
                    score = s * num
                    print(num, s, score, board.unmarked)
                    return score


def ints(line):
    return [int(x) for x in line.split(' ')]


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


def parse_bingo(lines):
    nums = [int(x) for x in lines[0].split(',')]
    boards = []
    board = []
    for i in range(2, len(lines)):
        line = lines[i]
        if not line:
            boards.append(board)
            board = []
        else:
            line = re.sub(r' +', ' ', line).lstrip()
            board.append(ints(line))

    return Bingo(nums, boards)


def solve(lines):
    bingo = parse_bingo(lines)
    return bingo.play()


def main():
    lines = read_lines(sys.argv[1])
    print(solve(lines))


if __name__ == '__main__':
    main()

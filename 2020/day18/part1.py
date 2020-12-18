#!/usr/bin/env python

import sys


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


class Tokenizer:
    def __init__(self, s):
        self.s = s
        self.index = 0

    def has_next(self):
        return self.index < len(self.s)

    def next(self):
        if self.s[self.index] == ' ':
            self.index += 1

        c = self.s[self.index]
        self.index += 1

        if '0' <= c <= '9':
            return int(c)

        return c


def parse_to_rpn(s):
    tokenizer = Tokenizer(s)
    out = []
    ops = []
    while tokenizer.has_next():
        token = tokenizer.next()
        if type(token) == int:
            out.append(token)
        elif token in '+*':
            while ops and ops[-1] != '(':
                out.append(ops.pop())
            ops.append(token)
        elif token == '(':
            ops.append(token)
        elif token == ')':
            while ops[-1] != '(':
                out.append(ops.pop())
            if ops[-1] == '(':
                ops.pop()

    while ops:
        out.append(ops.pop())

    return out


def myeval(s):
    rpn = parse_to_rpn(s)
    stack = []
    for token in rpn:
        if token == '+':
            op2 = stack.pop()
            op1 = stack.pop()
            stack.append(op1 + op2)
        elif token == '*':
            op2 = stack.pop()
            op1 = stack.pop()
            stack.append(op1 * op2)
        else:
            stack.append(token)

    return stack.pop()


def main():
    lines = read_lines(sys.argv[1])
    results = [myeval(s) for s in lines]
    print(sum(results))


if __name__ == '__main__':
    main()

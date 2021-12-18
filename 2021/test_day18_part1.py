import unittest

import utils

from day18_part1 import solve


class TestSolution(unittest.TestCase):
    def test_1_1_to_4_4(self):
        lines = '''
        [1,1]
[2,2]
[3,3]
[4,4]'''.split()
        self.assertEqual(solve(lines), 445)

    def test_1_1_to_5_5(self):
        lines = '''
        [1,1]
[2,2]
[3,3]
[4,4]
[5,5]'''.split()
        self.assertEqual(solve(lines), 791)

    def test_1_1_to_6_6(self):
        lines = '''
        [1,1]
[2,2]
[3,3]
[4,4]
[5,5]
[6,6]'''.split()
        self.assertEqual(solve(lines), 1137)

    def test_larger_example(self):
        lines = '''[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]'''.split()
        self.assertEqual(solve(lines), 3488)

    def test_input(self):
        lines = utils.read_lines("inputs/day18.txt")
        self.assertEqual(solve(lines), 3494)


if __name__ == '__main__':
    unittest.main()

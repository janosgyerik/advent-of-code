import unittest

from part1 import solve


class Test(unittest.TestCase):
    lines = ''''''.split()

    def test(self):
        self.assertEqual(solve(self.lines), 7)


if __name__ == '__main__':
    unittest.main()

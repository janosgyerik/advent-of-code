import unittest

from part2 import solve


class Test(unittest.TestCase):
    lines = '''199
200
208
210
200
207
240
269
260
263'''.split()

    def test(self):
        self.assertEqual(solve(self.lines), 5)


if __name__ == '__main__':
    unittest.main()

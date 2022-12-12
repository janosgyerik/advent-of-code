import unittest
from dataclasses import dataclass, field
from typing import List, Tuple

from bfs import bfs

DIRS = ((0, 1), (0, -1), (1, 0), (-1, 0))


def uphill(pos):
    r, c = pos
    e0 = INPUT.grid[r][c]

    for dr, dc in DIRS:
        r2, c2 = r + dr, c + dc
        if not (0 <= r2 < INPUT.rows and 0 <= c2 < INPUT.cols):
            continue

        e1 = INPUT.grid[r2][c2]
        if e1 <= e0 + 1:
            yield r2, c2


def downhill(pos):
    r, c = pos
    e0 = INPUT.grid[r][c]

    for dr, dc in DIRS:
        r2, c2 = r + dr, c + dc
        if not (0 <= r2 < INPUT.rows and 0 <= c2 < INPUT.cols):
            continue

        e1 = INPUT.grid[r2][c2]
        if e1 >= e0 - 1:
            yield r2, c2


class FindShortestPathLengthTest(unittest.TestCase):
    def test(self):
        def collectif(x):
            return x == INPUT.end

        self.assertEqual(((20, 72), 420), bfs(INPUT.start, uphill, collectif))


class FindShortestPathLengthsTest(unittest.TestCase):
    def test(self):
        def collectif(x):
            r, c = x
            return INPUT.grid[r][c] == ord('a')

        acc = []
        self.assertIsNone(bfs(INPUT.end, downhill, collectif, acc))
        self.assertEqual(((4, 0), 414), acc[0])
        self.assertEqual(((25, 0), 415), acc[1])
        self.assertEqual(((5, 2), 415), acc[2])


@dataclass
class Input:
    grid: List[List[int]]
    start: Tuple[int, int]
    end: Tuple[int, int]
    rows: int = field(init=False)
    cols: int = field(init=False)

    def __post_init__(self):
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])


def create_input():
    # 'S' marks the start, 'E' marks the end
    raw_grid = '''
    abcccccccccaaaaaaaaaaccccccccccccaaaaaaaaccaaccccccccccccccccccccccccccccccccccccccccccccaaaaaa
    abccccccccccaaaaaaaaaccccccccccccaaaaaaaaaaaacccccccccccaacccacccccccccccccccccccccccccccaaaaaa
    abcccccccccccaaaaaaacccccccccccccaaaaaaaaaaaaaacccccccccaaacaacccccccccaaaccccccccccccccccaaaaa
    abccccccccccaaaaaaccccccccccccccaaaaaaaaaaaaaaaccccccccccaaaaaccccccccccaaacccccccccccccccccaaa
    abccccccccccaaaaaaaccccccccccccaaaaaaaaaaaaaacccccccccccaaaaaacccccccccaaaacccccccccccccccccaac
    abaaccaaccccaaccaaaccccccccaaaaaaaaaaaaaaacaaccccccccccaaaaaaaacccccccccaaalcccccccccccccccaaac
    abaaaaaacccccccccaaccccccccaaaaaacccaaaacccaaccccccccccaaaaaaaaccccccccalllllllcccccccccccccccc
    abaaaaaacccccccaaacccccccccaaaaccccccaaaccccaaaaacccccccccaacccccccaaaakllllllllcccccccaacccccc
    abaaaaaacccccccaaaacccccccccaacccccccaaaccccaaaaacccccccccaacccccccaakkklllpllllccccacaaacccccc
    abaaaaaaaccccccaaaaccccaaccccccccccccccccccaaaaaaccccccccccccccccccckkkkpppppplllcccaaaaaaacccc
    abaaaaaaacaaaccaaaaccaaaaaaccccccccccccccccaaaaaacccccccaaaccccckkkkkkkpppppppplllcddaaaaaacccc
    abcaaaacccaacccccccccaaaaaacccccaaaccccccccaaaaaacccccccaaaaccjkkkkkkkpppppuppplmmdddddaaaccccc
    abccaaaaaaaaaccccccccaaaaaaccccaaaaaacccccccaaacccccccccaaaajjjkkkkkrpppuuuuupppmmmdddddacccccc
    abccccaaaaaaaacccccccaaaaacccccaaaaaacccccccccccccccccccaaacjjjjrrrrrrppuuuuupqqmmmmmddddaccccc
    abccccaaaaaaaaacccccccaaaacccccaaaaaaccccccccccccccccccccccjjjrrrrrrrrpuuuxuvvqqqmmmmmddddccccc
    abccccaaaaaaaaacccccccccccccccccaaaaaccccaacccaccccccccaaccjjjrrrruuuuuuuxxyvvqqqqqmmmmmdddcccc
    abccccaaaaaaaacccccccccaaaccccccaacaaccccaaacaacccaaacaaaccjjjrrrtuuuuuuuxxyvvvqqqqqmmmmdddcccc
    abccaaaaaaaacccccccccccaaaaaccccccccccccccaaaaacccaaaaaaaccjjjrrttttxxxxxxyyvvvvvqqqqmmmmdeeccc
    abccaaaccaaaccccccccaacaaaaacccccccccccccaaaaaacccaaaaaacccjjjrrtttxxxxxxxyyvvvvvvvqqqmmmeeeccc
    abaaaaaaaaaacccaaaccaaaaaaaaaaaccaaaccccaaaaaaaacccaaaaaaaajjjqqrttxxxxxxxyyyyyyvvvqqqnnneeeccc
    SbaaaaaaaaccccaaaaccaaaaaaaaaaaaaaaaacccaaaaaaaaccaaaaaaaaacjjjqqtttxxxxEzzyyyyvvvvqqqnnneeeccc
    abcaaaaaacccccaaaaccccaaaaaaaccaaaaaaccccccaaccccaaaaaaaaaaciiiqqqtttxxxyyyyyyvvvvrrrnnneeecccc
    abcaaaaaacccccaaaacccaaaaaaaaccaaaaaaccccccaaccccaaacaaacccciiiqqqqttxxyyyyyywvvvrrrnnneeeecccc
    abcaaaaaaccccccccccccaaaaaaaaacaaaaacccccccccccccccccaaaccccciiiqqtttxxyyyyyywwrrrrnnnneeeccccc
    abcaaacaacccccaacccccaaaaaaaaacaaaaacccccccccccccccccaaaccccciiiqqttxxxywwyyywwrrrnnnneeecccccc
    abccccccccaaacaaccccccccccacccccccccccccccccccccccccccccccccciiqqqttxxwwwwwwywwrrrnnneeeccccccc
    abccaacccccaaaaaccccccccccccccccccccccccccccccccccccccccaacaaiiqqqttwwwwsswwwwwrrrnnfffeccccccc
    abaaaaccccccaaaaaacccccccccccccccccccccccccccccaaaccccccaaaaaiiqqqttssssssswwwwrrronfffaccccccc
    abaaaaaacccaaaaaaacccccccccccccccccccccccccccaaaaaacccccaaaaaiiqqqssssssssssswrrrooofffaaaacccc
    abaaaaaaccaaaaaacccccccccccccccccccccccccccccaaaaaacccccaaaaaiiqqqppssspppssssrrrooofffaaaacccc
    abaaaaaaccaacaaacccccccccccccccccccccccccccccaaaaaacccccaaaaaiihpppppppppppossrrooofffaaaaacccc
    abaaaaccccccccaacccccccccccccccccccccccccccccaaaaaccccccccaaahhhhppppppppppoooooooofffaaaaccccc
    abaaaaccccccccccaacccccccccccccccccaaacccccccaaaaacccccccccccchhhhhhhhhhggpoooooooffffaaaaccccc
    abccaacccccccacaaaccccccccccccccccaaaaacccccccccccccccccccccccchhhhhhhhhggggoooooffffaacaaacccc
    abccccccccccaaaaacaaccccccccccccccaaaaaccccccccccccccccccccccccchhhhhhhhggggggggggffcaacccccccc
    abccccccccccaaaaaaaaccccccccccccccaaaacccaacccccccccccaccccccccccccccaaaaaggggggggfcccccccccccc
    abccccccccccccaaaaaccccaacccccccccaaaacaaaaccccccccaaaaccccccccccccccaaaacaaagggggcccccccccaccc
    abcccccccccccaaaaacccccaacccccccccaaaaaaaaaccccccccaaaaaaccccccccccccaaaccaaaacccccccccccccaaac
    abcccccccccccaacaaccaaaaaaaacccaaaaaaaaaaaccccccccccaaaaccccccccccccccaccccaaacccccccccccccaaaa
    abccccccccccccccaaccaaaaaaaaccaaaaaaaaaaaccccccccccaaaaacccccccccccccccccccccacccccccccccccaaaa
    abccccccccccccccccccccaaaaacccaaaaaaaaaaaacccccccccaacaacccccccccccccccccccccccccccccccccaaaaaa
    '''

    grid = [[ord(c) for c in row.strip()] for row in raw_grid.strip().splitlines()]
    start = end = None

    for r, row in enumerate(grid):
        for c, x in enumerate(row):
            if chr(x) == 'S':
                start = (r, c)
                grid[r][c] = ord('a')
            elif chr(x) == 'E':
                end = (r, c)
                grid[r][c] = ord('z')

    return Input(grid, start, end)


INPUT = create_input()

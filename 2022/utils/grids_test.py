import unittest

import grids


class GridTests(unittest.TestCase):
    def test_basic_properties(self):
        grid = grids.Grid(['.....', '.#...', '.....'])
        self.assertEqual(grid.rows, 3)
        self.assertEqual(grid.cols, 5)

    def test_print_string_valued_grid(self):
        lines = ['.....', '.#...', '.....']
        buffer = []
        grids.Grid(lines).print(sep=';', buffer=buffer)
        self.assertEqual(buffer, ['.;.;.;.;.', '.;#;.;.;.', '.;.;.;.;.'])

    def test_print_numeric_grid(self):
        lines = [[1] * 3, [2] * 3]
        buffer = []
        grids.Grid(lines).print(buffer=buffer)
        self.assertEqual(buffer, ['111', '222'])

    def test_constructor_raises_for_empty_grid(self):
        self.assertRaises(ValueError, lambda: grids.Grid([]))
        self.assertRaises(ValueError, lambda: grids.Grid([[]]))

    def test_constructor_raises_for_inconsistent_dimensions(self):
        self.assertRaises(ValueError, lambda: grids.Grid([[1] * 1, [2] * 2]))

    def test_loop_over_rows(self):
        lines = ['foo', 'bar', 'baz']
        grid = grids.Grid(lines)
        it = (row for row in grid)
        self.assertEqual(lines[0], next(it))
        self.assertEqual(lines[1], next(it))
        self.assertEqual(lines[2], next(it))

    def test_index_rows(self):
        lines = ['foo', 'bar', 'baz']
        grid = grids.Grid(lines)
        self.assertEqual(lines[0], grid[0])
        self.assertEqual(lines[1], grid[1])

    def test_index_rows_and_cols(self):
        lines = ['foo', 'bar', 'baz']
        grid = grids.Grid(lines)
        self.assertEqual(lines[0][0], grid[0][0])

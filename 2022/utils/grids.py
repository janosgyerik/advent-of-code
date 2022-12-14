class Grid:
    def __init__(self, grid):
        if not (len(grid) and len(grid[0])):
            raise ValueError(f"Grid must not be empty! Got: {grid}")

        self.grid = grid
        self._string_valued = isinstance(grid[0][0], str)
        self._rows = len(grid)
        self._cols = len(grid[0])

        if not all(len(row) == self.cols for row in grid):
            raise ValueError(f"All rows must have the same number of columns!")

    @property
    def rows(self):
        return self._rows

    @property
    def cols(self):
        return self._cols

    def __iter__(self):
        return GridIter(self.grid)

    def __getitem__(self, item):
        return self.grid[item]

    def print(self, sep='', buffer=None):
        def strings_to_line(strings):
            return sep.join(strings)

        def items_to_line(items):
            return sep.join(str(x) for x in items)

        if self._string_valued:
            to_line_fn = strings_to_line
        else:
            to_line_fn = items_to_line

        def collect_to_buffer(line):
            buffer.append(line)

        if isinstance(buffer, list):
            print_fn = collect_to_buffer
        else:
            print_fn = print

        for row in self.grid:
            print_fn(to_line_fn(row))


class GridIter:
    def __init__(self, grid):
        self.grid = grid
        self._current_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._current_index < len(self.grid):
            row = self.grid[self._current_index]
            self._current_index += 1
            return row

        raise StopIteration

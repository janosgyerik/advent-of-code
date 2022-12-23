def neighbors(*coords):
    for i in range(len(coords)):
        copy = list(coords)
        copy[i] += 1
        yield tuple(copy)

        copy = list(coords)
        copy[i] -= 1
        yield tuple(copy)


def neighbors_all(x, y):
    yield -1, -1
    yield -1, 0
    yield -1, 1
    yield 1, -1
    yield 1, 0
    yield 1, 1
    yield 0, -1
    yield 0, 1


def manhattan_distance(*pairs):
    halflen = len(pairs) // 2
    return sum(abs(x1 - x2) for x1, x2 in zip(pairs[:halflen], pairs[halflen:]))

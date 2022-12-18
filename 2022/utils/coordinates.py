def neighbors(*coords):
    for i in range(len(coords)):
        copy = list(coords)
        copy[i] += 1
        yield tuple(copy)

        copy = list(coords)
        copy[i] -= 1
        yield tuple(copy)

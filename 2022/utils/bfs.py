from collections import deque


def never(item):
    return False


def bfs(start, childrenfn, collectif=never, acc=None):
    q = deque([start])
    seen = {start}
    depth = 0

    while q:
        for _ in range(len(q)):
            current = q.popleft()
            if collectif(current):
                if acc is None:
                    return current, depth
                else:
                    acc.append((current, depth))
                    continue

            for child in childrenfn(current):
                if child in seen:
                    continue

                seen.add(child)
                q.append(child)

        depth += 1

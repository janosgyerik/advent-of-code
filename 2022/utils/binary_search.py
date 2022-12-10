def binary_search(items, target, key):
    left = 0
    right = len(items)
    while left < right:
        mid = left + (right - left) // 2
        current = key(mid)
        if target < current:
            right = mid
        else:
            left = mid + 1

    return items[left - 1]

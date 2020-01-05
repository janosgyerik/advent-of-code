#!/usr/bin/env python3

import sys


def compute_prefix_sum(nums):
    psums = [0]
    total = 0
    for num in nums:
        total += num
        psums.append(total)
    return psums


def apply_pattern(psums, length):
    start = length-1
    positive = True
    total = 0
    while start < len(psums) - 1:
        end = min(len(psums) - 1, start + length)
        subtotal = psums[end] - psums[start]
        if not positive:
            subtotal = -subtotal
        total += subtotal
        start += length * 2
        positive = not positive

    return abs(total) % 10


def fft(digits):
    out = [0] * len(digits)
    psums = compute_prefix_sum(digits)
    for pos in range(len(digits)):
        rep = pos + 1
        out[pos] = apply_pattern(psums, rep)
    return out


def main():
    line = sys.stdin.read().rstrip()
    digits = [int(x) for x in line] * 10000
    offset = int(''.join(str(x) for x in digits[:7]))
    for i in range(100):
        digits = fft(digits)
    print(''.join(str(x) for x in digits[offset:offset+8]))


if __name__ == '__main__':
    main()

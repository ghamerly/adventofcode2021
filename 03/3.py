#!/usr/bin/env python3

# https://adventofcode.com/2021/day/3
# Author: Greg Hamerly

def part1(cmds):
    bits = zip(*map(str.strip, cmds))

    gamma = epsilon = 0
    for row in bits:
        gamma *= 2
        epsilon *= 2

        zeros = row.count('0')
        ones = row.count('1')
        assert zeros != ones

        if zeros < ones:
            gamma += 1
        else:
            epsilon += 1

    return gamma * epsilon

def part2_sub(rows, f):
    remaining = list(range(len(rows)))
    pos = 0

    # keep filtering out the remaining indexes of the given rows until exactly
    # one is left (the problem is designed to end with exactly one)
    while len(remaining) > 1:
        # look at the bits in the current position
        bits = [rows[i][pos] for i in remaining]
        zeros = bits.count('0')
        ones = bits.count('1')
        remaining = [i for i in remaining if rows[i][pos] == f(zeros, ones)]
        pos += 1

    assert len(remaining) == 1

    # parse this number as base-2
    return int(rows[remaining[0]], 2)

def part2(cmds):
    rows = list(map(str.strip, cmds))

    # keep only the most common bit; use 1 if there's a tie
    most_common = lambda zeros, ones: '1' if zeros <= ones else '0' 
    o2 = part2_sub(rows, most_common)

    # keep only the least common bit; use 0 if there's a tie
    least_common = lambda zeros, ones: '0' if zeros <= ones else '1' 
    co2 = part2_sub(rows, least_common)

    return o2 * co2

def main():
    with open('3.in') as f:
        cmds = list(f)

    print('part 1:', part1(cmds))
    print('part 2:', part2(cmds))

if __name__ == '__main__':
    main()

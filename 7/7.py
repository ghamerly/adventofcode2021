#!/usr/bin/env python3

# https://adventofcode.com/2021/day/7 -- "crab fuel"
# Author: Greg Hamerly

import sys

def least_fuel_linear(positions, cost):
    '''Turn a list of positions into a list of positions and counts. Then score
    each of those positions according to the given cost function, and return the
    minimum score over all positions.

    This was my first solution, but I was not satisfied with it. So I wrote the
    ternary search below.'''
    pos_count = {p: positions.count(p) for p in positions}
    score = lambda pos: sum(cost(abs(p - pos)) * count for p, count in pos_count.items())
    return min(map(score, range(min(pos_count), max(pos_count) + 1)))

def least_fuel_ternary(positions, cost):
    '''The problem does not explicitly say that the positions must be integers;
    we can sometimes find a lower cost using a non-integer cost. The cost
    function is unimodal, so ternary search is appropriate and fast.

    But, since the problem implicitly seems to require integer position answers,
    use the best position to find the best nearest integer position.'''
    positions = {p: positions.count(p) for p in positions}
    score = lambda pos: sum(cost(abs(p - pos)) * positions[p] for p in positions)

    low, high = min(positions), max(positions)
    while low + 0.000000001 < high:
        a = low + (high - low) / 3
        b = low + (high - low) * 2 / 3
        if score(a) < score(b):
            high = b
        else:
            low = a

    # but search around that best position for the integer position with the
    # best cost
    x = int(low)
    return min(map(score, [x - 1, x, x + 1]))

# use ternary search
least_fuel = least_fuel_ternary

def part1(positions):
    '''The cost is just the distance.'''
    return least_fuel(positions, lambda x: x)

def part2(positions):
    '''The cost is n(n+1)/2 for a distance of n, because of the identity
    sum(1,2,...,n) = n(n+1)/2.'''
    return least_fuel(positions, lambda x: x * (x + 1) // 2)

def main():
    regular_input = __file__.split('/')[-1][:-len('.py')] + '.in'
    file = regular_input if len(sys.argv) <= 1 else sys.argv[1]
    print(f'using input: {file}')
    with open(file) as f:
        lines = list(f)

    positions = list(map(int, lines[0].split(',')))

    print('part 1:', part1(positions))
    print('part 2:', part2(positions))

if __name__ == '__main__':
    main()

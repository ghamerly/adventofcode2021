#!/usr/bin/env python3

# https://adventofcode.com/2021/day/6 ("lanternfish")
# Author: Greg Hamerly

import collections
import sys

def simulate(init_counts, days):
    '''Simulate 'days' steps according to the rules given in the problem:
        - each fish steps down by one count each day
        - when a fish reaches zero, it respawns with a count of 6 and creates
          another new fish with a count of 8
    Speed things up significantly by grouping all fish of the same count.'''
    counts = {f: init_counts.count(f) for f in init_counts}
    for i in range(days):
        new_counts = collections.defaultdict(int)
        for f, count in counts.items():
            if f == 0:
                new_counts[6] += count
                new_counts[8] += count
            else:
                new_counts[f-1] += count
        counts = new_counts

    return sum(counts.values())

def part1(init_counts):
    '''Do a simulation for 80 days'''
    return simulate(init_counts, 80)

def part2(init_counts):
    '''Do a simulation for 256 days'''
    return simulate(init_counts, 256)

def main():
    regular_input = __file__.split('/')[-1][:-len('.py')] + '.in'
    file = regular_input if len(sys.argv) <= 1 else sys.argv[1]
    print(f'using input: {file}')
    with open(file) as f:
        lines = list(f)

    init_counts = list(map(int, lines[0].split(',')))

    print('part 1:', part1(init_counts))
    print('part 2:', part2(init_counts))

if __name__ == '__main__':
    main()

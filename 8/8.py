#!/usr/bin/env python3

# https://adventofcode.com/2021/day/8 - "seven segment"
# Author: Greg Hamerly

# This code is really overkill. There are way too many sorts, and I'm sure
# there's a faster way than brute-forcing every permutation. But it's 1 AM and
# I'm a working father.

import itertools
import sys

def part1(lines):
    '''This part is simple, just count how many of the numbers have 2, 3, 4, or
    7 segments turned on (which uniquely identify the digits 1, 7, 4, and 8
    respectively).'''
    ans = 0
    for line in lines:
        a, b = line.split(' | ')
        on = b.split()
        for n in on:
            if len(n) in [2, 3, 4, 7]:
                ans += 1
    return ans

#  0:      1:      2:      3:      4:
#  aaaa    ....    aaaa    aaaa    ....
# b    c  .    c  .    c  .    c  b    c
# b    c  .    c  .    c  .    c  b    c
#  ....    ....    dddd    dddd    dddd
# e    f  .    f  e    .  .    f  .    f
# e    f  .    f  e    .  .    f  .    f
#  gggg    ....    gggg    gggg    ....
# 
#   5:      6:      7:      8:      9:
#  aaaa    aaaa    aaaa    aaaa    aaaa
# b    .  b    .  .    c  b    c  b    c
# b    .  b    .  .    c  b    c  b    c
#  dddd    dddd    ....    dddd    dddd
# .    f  e    f  .    f  e    f  .    f
# .    f  e    f  .    f  e    f  .    f
#  gggg    gggg    ....    gggg    gggg

# init global tables
SEGMENTS = {
        0: 'abcefg',
        1: 'cf',
        2: 'acdeg',
        3: 'acdfg',
        4: 'bcdf',
        5: 'abdfg',
        6: 'abdefg',
        7: 'acf',
        8: 'abcdefg',
        9: 'abcdfg'
        }

SEGMENTS_REV = {pattern: digit for digit, pattern in SEGMENTS.items()}

def consistent(permutation, ten_patterns):
    '''Identify whether the permutation (ordering of a-g) is consistent with the
    ten patterns given in the line.'''
    for pattern in SEGMENTS.values():
        mapped_pattern = ''.join(sorted([permutation[ord(c)-ord('a')] for c in pattern]))
        if mapped_pattern not in ten_patterns:
            return False
    return True

def find_permutation(ten_patterns):
    '''Try all 5040 possible permutations of the letters a-g, and identify the
    one that is consistent with the given patterns.

    A faster-running method would likely be to recursively build the
    permutation, and prune the search as soon as we find an inconsistent
    permutation prefix.
    '''
    answer = []
    for permutation in itertools.permutations('abcdefg', 7):
        if consistent(permutation, ten_patterns):
            answer.append(permutation)
            # we could break here... but for sanity we check that we only find
            # one consistent permutation

    assert len(answer) == 1, answer
    return answer[0]

def part2(lines):
    '''Find a permutation of the segments that is consistent with the data, use
    that to build a 4-digit number, and add up those 4-digit numbers.'''
    ans = 0
    for line in lines:
        ten_patterns, numbers = line.split(' | ')
        ten_patterns = [''.join(sorted(w)) for w in ten_patterns.split()]
        numbers = numbers.split()

        # brute-force a solution...
        mapping = find_permutation(ten_patterns)

        s = 0
        for n in numbers:
            # sanity checking
            #n_sorted = ''.join(sorted(n))
            #assert n_sorted in ten_patterns

            # invert the mapping to look up the digit
            n_mapped = ''.join(sorted(['abcdefg'[mapping.index(c)] for c in n]))
            s = s * 10 + SEGMENTS_REV[n_mapped]
        ans += s

    return ans

def main():
    regular_input = __file__.split('/')[-1][:-len('.py')] + '.in'
    file = regular_input if len(sys.argv) <= 1 else sys.argv[1]
    print(f'using input: {file}')
    with open(file) as f:
        lines = list(f)

    print('part 1:', part1(lines))
    print('part 2:', part2(lines))

if __name__ == '__main__':
    main()

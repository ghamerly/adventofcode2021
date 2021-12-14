#!/usr/bin/env python3

# https://adventofcode.com/2021/day/14 - "extended polymerization"
# Author: Greg Hamerly

# Use grammar rules to roughly double the length of a string for a certain
# number of iterations.

import sys
import collections

def efficient(start, rules, iterations):
    '''Keep track of each pair of letters and their counts. Update the pair
    counts by applying the rule:
        AB -> C
    so that pair AB produces AC and BC with the same counts as the original
    AB.

    After iterating the given number of times, count among the pairs how many
    times each single character occurs (counting only the first among each pair,
    and the special last character of the original string).
    '''

    # initialize the pair counts
    pairs = collections.defaultdict(int)
    for i in range(len(start) - 1):
        pairs[start[i:i+2]] += 1

    for _ in range(iterations):
        next_pairs = collections.defaultdict(int)
        for pair, cnt in pairs.items():
            next_pairs[pair[0] + rules[pair]] += cnt
            next_pairs[rules[pair] + pair[1]] += cnt

        # sanity checking
        a = sum(pairs.values())
        b = sum(next_pairs.values())
        assert a * 2 == b, (a, b, pairs, next_pairs)

        pairs = next_pairs

    # now count the number of unique elements -- the first one from each pair,
    # plus the last element (which is left out of the loop)
    element_count = collections.defaultdict(int)
    for pair, cnt in pairs.items():
        element_count[pair[0]] += cnt
    # the original last character is still the last character of the
    # hypothetical production, since it never was the initial part of any pair
    element_count[start[-1]] += 1

    return max(element_count.values()) - min(element_count.values())

def brute_force(start, rules, iterations):
    '''Apply the rules by direct simulation. Works for a small number of
    iterations (e.g. part 1), but the string gets as long as O(2^{iterations}),
    so it becomes too slow for a large number of iterations (e.g. > 20).'''
    p = start
    for _ in range(iterations):
        next_p = []
        for j in range(len(p) - 1):
            next_p.append(p[j]) # original letter
            next_p.append(rules[p[j:j+2]]) # inserted letter
        next_p.append(p[-1])
        p = ''.join(next_p)

    element_count = {c: p.count(c) for c in p}
    return max(element_count.values()) - min(element_count.values())

def part1(start, rules):
    '''Run for 10 iterations. Brute-force sanity check as well.'''
    assert brute_force(start, rules, 10) == efficient(start, rules, 10)
    return efficient(start, rules, 10)

def part2(start, rules):
    '''Run for 40 iterations.'''
    return efficient(start, rules, 40)

def main():
    regular_input = __file__.split('/')[-1][:-len('.py')] + '.in'
    file = regular_input if len(sys.argv) <= 1 else sys.argv[1]
    print(f'using input: {file}')
    with open(file) as f:
        lines = list(map(str.strip, f))

    # parse the input
    start = lines[0]
    f = lambda l: l.split(' -> ')
    rules = dict(map(f, lines[2:]))
    assert len(rules) + 2 == len(lines)

    print('part 1:', part1(start, rules))
    print('part 2:', part2(start, rules))

if __name__ == '__main__':
    main()

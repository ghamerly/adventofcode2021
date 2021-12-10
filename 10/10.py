#!/usr/bin/env python3

# https://adventofcode.com/2021/day/10 - "balancing parentheses"
# Author: Greg Hamerly

# I actually got 31st overall on the first task (see
# https://adventofcode.com/2021/leaderboard/day/10); a stupid variable
# initialization bug where I forgot to reset the stack cost me a lot on the
# second task.

import sys

def parse(line, mismatch=None, complete=None):
    '''Try to balance the parentheses on the line. Stop when we get a mismatch
    (and call the function "mismatch" with the offending character) or when we
    get to the end of the line (and call the function "complete" with the
    current stack).'''
    s = []
    m = { ')': '(', ']': '[', '>': '<', '}': '{' }
    for c in line:
        if c in '({[<':
            s.append(c)
        elif s and m[c] == s[-1]:
            s.pop()
        else:
            if mismatch:
                return mismatch(c)
            break
    else:
        if complete:
            return complete(s)

def part1(lines):
    '''Add up the values associated with the first closing characters on each
    line that are incorrectly balanced (if any).'''
    score = { ')': 3, ']': 57, '}': 1197, '>': 25137 }
    return sum(filter(None, [parse(line, score.__getitem__) for line in lines]))

def part2(lines):
    '''Add up the values computed from completing each line that had some open
    parentheses left after a correctly-parsed line.'''
    def complete(s):
        score = { '(': 1, '[': 2, '{': 3, '<': 4 }
        line_score = 0
        while s:
            line_score = line_score * 5 + score[s.pop()]
        return line_score

    p = lambda l: parse(l, complete=complete)
    scores = sorted(filter(None, map(p, lines)))
    return scores[len(scores) // 2]

def main():
    regular_input = __file__.split('/')[-1][:-len('.py')] + '.in'
    file = regular_input if len(sys.argv) <= 1 else sys.argv[1]
    print(f'using input: {file}')
    with open(file) as f:
        lines = list(f)

    lines = list(map(str.strip, lines))

    print('part 1:', part1(lines))
    print('part 2:', part2(lines))

if __name__ == '__main__':
    main()

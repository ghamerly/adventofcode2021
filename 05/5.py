#!/usr/bin/env python3

# https://adventofcode.com/2021/day/5 ("count intersections")
# Author: Greg Hamerly

import sys

def count_intersections(lines, use_line):
    '''Iterate over each line (rasterizing the lines) and count the number of
    points where more than one line touches. Filter out lines using the provided
    use_line function.'''
    counts = {}

    # determine the step for endpoints a and b
    step = lambda a, b: 0 if a == b else (b - a) // abs(b - a)

    for (ax, ay), (bx, by) in lines:
        if not use_line(ax, ay, bx, by):
            continue

        dx, dy = step(ax, bx), step(ay, by)

        # make sure the line is horizontal, vertical, or diagonal
        assert dx in (-1, 0, 1) and dy in (-1, 0, 1)
        assert dx != 0 or dy != 0

        x, y = ax, ay
        while x != bx + dx or y != by + dy:
            counts[(x, y)] = counts.get((x, y), 0) + 1
            x, y = x + dx, y + dy

    intersections = [c for c in counts.values() if c >= 2]
    return len(intersections)

def part1(lines):
    '''Count intersections of only horizontal lines.'''
    return count_intersections(lines, lambda ax, ay, bx, by: ax == bx or ay == by)

def part2(lines):
    '''Count intersections of all given lines.'''
    return count_intersections(lines, lambda *x: True)

def parse(line):
    '''Parse the line into two pairs, parsing integers.'''
    a, b, c = line.split()
    start = tuple(map(int, a.split(',')))
    end = tuple(map(int, c.split(',')))

    return (start, end)

def main():
    regular_input = __file__.split('/')[-1][:-len('.py')] + '.in'
    file = regular_input if len(sys.argv) <= 1 else sys.argv[1]
    print(f'using input: {file}')
    with open(file) as f:
        lines = list(f)

    lines = list(map(parse, lines))

    print('part 1:', part1(lines))
    print('part 2:', part2(lines))

if __name__ == '__main__':
    main()

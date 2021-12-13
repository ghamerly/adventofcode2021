#!/usr/bin/env python3

# https://adventofcode.com/2021/day/13 - "transparent origami"
# Author: Greg Hamerly

import sys

def display(points):
    '''Render the current board as a grid.'''
    max_y = max(y for x, y in points)
    max_x = max(x for x, y in points)
    out = []
    for y in range(max_y + 1):
        out.append(''.join(' #'[(x,y) in points] for x in range(max_x + 1)))
    return '\n'.join(out)

def fold(lines, stop_after):
    '''Parse the points in "lines" until reaching a blank line, then follow the
    folding instructions until reaching "stop_after" folds. Return the resulting
    set of points after that many folds.'''

    blank = lines.index('')
    points = {tuple(map(int, l.split(','))) for l in lines[:blank]}

    fold_start = blank + 1
    for fold_instruction in lines[fold_start:fold_start+stop_after]:
        axis, value = fold_instruction.split()[-1].split('=')
        value = int(value)

        # Mirror the x values depending on what the fold axis is and the value.
        # If the fold axis is y, or x < value, do nothing.  Otherwise, flip it
        # by value-(x-value) = 2*value-x.
        fx = lambda x: x if axis == 'y' or x < value else 2 * value - x
        # The same logic, but for y.
        fy = lambda y: y if axis == 'x' or y < value else 2 * value - y
        points = {(fx(x), fy(y)) for x, y in points}

    return points

def part1(lines):
    '''Find the number of points left after just the first fold.'''
    return len(fold(lines, 1))

def part2(lines):
    '''Display how the paper looks after all the folds have been made.'''
    points = fold(lines, len(lines))
    return '\n' + display(points)

def main():
    regular_input = __file__.split('/')[-1][:-len('.py')] + '.in'
    file = regular_input if len(sys.argv) <= 1 else sys.argv[1]
    print(f'using input: {file}')
    with open(file) as f:
        lines = list(map(str.strip, f))

    print('part 1:', part1(lines))
    print('part 2:', part2(lines))

if __name__ == '__main__':
    main()

#!/usr/bin/env python3

# https://adventofcode.com/2021/day/25 - "sea cucumber"
# Author: Greg Hamerly

import sys

def part1(seafloor, height, width):
    num_iterations = 0
    moved = True
    while moved:
        moved = False
        sf_next = {}

       # display the state
       #print(num_iterations)
       #for i in range(height):
       #    row = [seafloor.get((i, j), '.') for j in range(width)]
       #    print(''.join(row))

        # east
        for (i, j), direction in seafloor.items():
            if direction == 'v':
                continue

            jj = (j + 1) % width
            if (i, jj) in seafloor:
                sf_next[(i, j)] = '>'
            else:
                sf_next[(i, jj)] = '>'
                moved = True

        # south
        for (i, j), direction in seafloor.items():
            if direction == '>':
                continue

            ii = (i + 1) % height
            if seafloor.get((ii, j), '') == 'v' or (ii, j) in sf_next:
                sf_next[(i, j)] = 'v'
            else:
                sf_next[(ii, j)] = 'v'
                moved = True

        num_iterations += 1
        seafloor = sf_next

    return num_iterations

def main():
    regular_input = __file__.split('/')[-1][:-len('.py')] + '.in'
    file = regular_input if len(sys.argv) <= 1 else sys.argv[1]
    print(f'using input: {file}')
    with open(file) as f:
        lines = list(map(str.strip, f))

    seafloor = {}
    height, width = len(lines), len(lines[0])
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c == '.':
                continue
            seafloor[(i,j)] = c

    print('part 1:', part1(seafloor, height, width))

if __name__ == '__main__':
    main()

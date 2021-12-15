#!/usr/bin/env python3

# https://adventofcode.com/2021/day/15 - "chiton"
# Author: Greg Hamerly

import heapq
import sys

def dijkstra(cave):
    '''Use Dijkstra's algorithm to find the shortest path from the top left of
    the "cave" to the bottom right, where the cost ("risk") of each step is the
    value of the cell being entered. For some reason, entering the starting cell
    costs 0 (according to the problem statement).'''

    rows = len(cave)
    cols = len(cave[0])

    # (row, col): min-cost
    cost = {(i, j): 1e100 for i in range(rows) for j in range(cols)}
    cost[(0, 0)] = 0
    # We could make lookups into "cost" (and the overall algorithm)
    # significantly faster by combining each coordinate pair (i, j) into a
    # single index, e.g. (i * cols + j), but that makes the code more confusing.

    # min-heap: (cost, row, col)
    frontier = [(0, 0, 0)]

    while frontier:
        c, i, j = heapq.heappop(frontier)
        for ii, jj in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
            if 0 <= ii < rows and 0 <= jj < cols:
                cc = c + cave[ii][jj]
                if cc < cost[(ii, jj)]:
                    cost[(ii, jj)] = cc
                    heapq.heappush(frontier, (cc, ii, jj))

    return cost[(rows-1, cols-1)]

def part1(cave):
    '''Just find the shortest path from the top left to the bottom right.'''
    return dijkstra(cave)

def part2(cave):
    '''Multiply the cave 25 times (5x5), adding 1 to each cell for each "step"
    away from the original cave copy (i.e. top left copy adds 0, the 2 copies to
    the right and below that one add 1, the copies one more step away from those
    two add 2, etc.). Wrap cell value x > 9 back around to (x % 10) + 1.  Then
    find the shortest path in that cave from the top left to the bottom
    right.'''
    rows = len(cave)
    cols = len(cave[0])

    cave_5x5 = [[None] * cols * 5 for _ in range(rows * 5)]
    for i in range(rows * 5):
        ii, io = i % rows, i // rows
        for j in range(cols * 5):
            jj, jo = j % cols, j // cols
            cave_5x5[i][j] = (cave[ii][jj] + io + jo - 1) % 9 + 1

    return dijkstra(cave_5x5)

def main():
    regular_input = __file__.split('/')[-1][:-len('.py')] + '.in'
    file = regular_input if len(sys.argv) <= 1 else sys.argv[1]
    print(f'using input: {file}')
    with open(file) as f:
        lines = list(map(str.strip, f))

    cave = [list(map(int, line)) for line in lines]

    print('part 1:', part1(cave))
    print('part 2:', part2(cave))

if __name__ == '__main__':
    main()

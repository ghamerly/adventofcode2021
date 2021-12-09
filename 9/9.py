#!/usr/bin/env python3

# https://adventofcode.com/2021/day/9 - "lava tubes"
# Author: Greg Hamerly

import itertools
import sys

def low_points(heightmap):
    '''Find all the 'low points', which are defined as those cells in the
    heightmap that are lower than all 4 NSEW adjacent cells (of those that
    exist).'''
    on_map = lambda i, j: 0 <= i < len(heightmap) and 0 <= j < len(heightmap[i])
    
    for i, row in enumerate(heightmap):
        for j, col in enumerate(row):
            for ii, jj in [(i-1,j), (i+1,j), (i,j-1), (i,j+1)]:
                if (ii == i and jj == j) or not on_map(ii, jj):
                    continue
                if heightmap[ii][jj] <= heightmap[i][j]:
                    break
            else:
                yield (i, j)

def part1(heightmap):
    '''Sum the heights of each of the low points (adding one to the height of
    each of them before summing).'''
    return sum(heightmap[i][j] + 1 for (i, j) in low_points(heightmap))

def basin_size_nonrec(heightmap, seen, i, j):
    '''Fill in the basin, starting at (i, j), and return the number of cells
    belonging to the basin. Uses non-recursive DFS.'''
    assert (i, j) not in seen
    q = [(i, j)]
    seen.add((i, j))
    size = 1
    on_map = lambda i, j: 0 <= i < len(heightmap) and 0 <= j < len(heightmap[i])
    while q:
        i, j = q.pop()
        for ii, jj in [(i-1,j), (i+1,j), (i,j-1), (i,j+1)]:
            # the problem defines 9 as a boundary for basins
            if on_map(ii, jj) and heightmap[ii][jj] != 9 and (ii,jj) not in seen:
                seen.add((ii, jj))
                size += 1
                q.append((ii, jj))
    return size

def basin_size_rec(heightmap, seen, i, j):
    '''Fill in the basin, starting at (i, j), and return the number of cells
    belonging to the basin. Uses recursive DFS.'''
    assert (i, j) not in seen
    seen.add((i, j))
    on_map = lambda i, j: 0 <= i < len(heightmap) and 0 <= j < len(heightmap[i])
    size = 1
    for ii, jj in [(i-1,j), (i+1,j), (i,j-1), (i,j+1)]:
        # the problem defines 9 as a boundary for basins
        if on_map(ii, jj) and heightmap[ii][jj] != 9 and (ii,jj) not in seen:
            size += basin_size_rec(heightmap, seen, ii, jj)
    return size

basin_size = basin_size_nonrec

def part2(heightmap):
    '''Find the sizes of all the basins, and return the product of the sizes of
    three largest basins.'''
    seen = set()
    sizes = sorted(basin_size(heightmap, seen, i, j) for (i, j) in low_points(heightmap))
    return sizes[-3] * sizes[-2] * sizes[-1]

def main():
    regular_input = __file__.split('/')[-1][:-len('.py')] + '.in'
    file = regular_input if len(sys.argv) <= 1 else sys.argv[1]
    print(f'using input: {file}')
    with open(file) as f:
        lines = list(f)

    heightmap = [list(map(int, line.strip())) for line in lines]

    print('part 1:', part1(heightmap))
    print('part 2:', part2(heightmap))

if __name__ == '__main__':
    main()

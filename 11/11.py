#!/usr/bin/env python3

# https://adventofcode.com/2021/day/11 - "flashing octopi"
# Author: Greg Hamerly

import sys

def iterate_board(board, max_iters, flashed_functor):
    '''Iterate the process described in the problem of adding one to every cell,
    and "flashing" whenever a cell reaches 10. Flashes add one to neighboring
    cells, which may cause them to flash, etc. No cell may flash more than once
    per iteration. Iterate for max_iters (at most), and call flashed_functor
    with the current iteration and the number of flashed cells. Stop iterating
    early if flashed_functor returns True.'''

    for iteration in range(1, max_iters + 1):
        # add one to each cell and find the initial set of flashes
        flashes = []
        flashed = set()
        bnew = [[ri + 1 for ri in row] for row in board]
        for i, row in enumerate(bnew):
            for j, col in enumerate(row):
                if col >= 10:
                    flashes.append((i, j))
                    flashed.add((i, j))
                    bnew[i][j] = 0

        # now do a sort of BFS for all other flashes
        while flashes:
            new_flashes = []
            for i, j in flashes:
                for ii in range(i-1, i+2):
                    for jj in range(j-1, j+2):
                        if ii == i and jj == j or (ii, jj) in flashed:
                            continue
                        if not (0 <= ii < len(bnew) and 0 <= jj < len(bnew[ii])):
                            continue

                        bnew[ii][jj] += 1
                        if bnew[ii][jj] >= 10:
                            new_flashes.append((ii, jj))
                            flashed.add((ii, jj))
                            bnew[ii][jj] = 0

            flashes = new_flashes

        board = bnew

        # call the given functor
        if flashed_functor(iteration, len(flashed)):
            return

def part1(board):
    '''Add up all the flashes that occur in 100 iterations.'''
    ans = 0
    def sum_flashed(_, flashed):
        nonlocal ans
        ans += flashed
    iterate_board(board, 100, sum_flashed)
    return ans

def part2(board):
    '''Identify the first iteration where all cells flash'''
    ans = None
    def all_flashed(iteration, flashed):
        nonlocal ans
        if flashed == len(board) * len(board[0]):
            ans = iteration
            return True
    iterate_board(board, 10000, all_flashed)
    return ans

def main():
    regular_input = __file__.split('/')[-1][:-len('.py')] + '.in'
    file = regular_input if len(sys.argv) <= 1 else sys.argv[1]
    print(f'using input: {file}')
    with open(file) as f:
        lines = list(map(str.strip, f))

    board = [list(map(int, line)) for line in lines]

    print('part 1:', part1(board))
    print('part 2:', part2(board))

if __name__ == '__main__':
    main()

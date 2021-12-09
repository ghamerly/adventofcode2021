#!/usr/bin/env python3

# https://adventofcode.com/2021/day/4 ("Bingo")
# Author: Greg Hamerly

import sys

def board_wins(board):
    '''return true if any row or column sums to -5'''
    return -5 in map(sum, board + list(zip(*board)))

def score(board, n):
    '''score is defined by the problem to be the sum of non-marked numbers times
    the last number called (n)'''
    # count non-marked entries by zeroing out the -1s
    f = lambda x: max(0, x)
    s = sum(sum(map(f, row)) for row in board)
    return s * n

def iterate_wins(numbers_called, boards):
    '''keep calling numbers; yielding each board once it achieves a win'''
    already_won = set()
    for n in numbers_called:
        for board_ndx, board in enumerate(boards):
            if board_ndx in already_won:
                continue

            for row in board:
                if n in row:
                    row[row.index(n)] = -1
                    break

            if board_wins(board):
                already_won.add(board_ndx)
                yield (board_ndx, n)

def part1(numbers_called, boards):
    '''stop when the first board has won''' 
    for board_ndx, n in iterate_wins(numbers_called, boards):
        return score(boards[board_ndx], n)

def part2(numbers_called, boards):
    '''stop when the last board has won''' 
    for board_ndx, n in iterate_wins(numbers_called, boards):
        pass
    # use the fact that the last iteration's values are still available
    return score(boards[board_ndx], n)

def main():
    regular_input = __file__.split('/')[-1][:-len('.py')] + '.in'
    file = regular_input if len(sys.argv) <= 1 else sys.argv[1]
    print(f'using input: {file}')
    with open(file) as f:
        lines = list(f)

    numbers_called = list(map(int, lines[0].split(',')))
    boards = []
    for index in range(2, len(lines), 6):
        boards.append([list(map(int, row.split())) for row in lines[index:index+5]])
        # assure the numbers are unique in each board
        assert len(set(sum(boards[-1], []))) == 25

    print('part 1:', part1(numbers_called, boards))
    print('part 2:', part2(numbers_called, boards))

if __name__ == '__main__':
    main()

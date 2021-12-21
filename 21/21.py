#!/usr/bin/env python3

# https://adventofcode.com/2021/day/21 - "dirac dice"
# Author: Greg Hamerly

import sys

def part1(lines):
    '''Repeatedly roll a deterministic 100-sided die, following the rules of
       the game. Each player starts from some position, rolls thrice, moves
       around the board (the board has 10 spots, and wraps around). Each time,
       add to the score the value of the square landed on. Stop when a player
       reaches at least 1000, and report a hash of the game.'''
    positions = [int(line.split()[-1]) for line in lines]
    scores = [0, 0]

    rolls = 0
    while max(scores) < 1000: # the game ends when any player reaches 1000 or more
        # the dice are deterministic, so each move's distance is as follows
        dist = rolls * 3 + 6

        # 3 rolls per player, so the player is determined as the number of
        # rolls mod 2
        player = rolls % 2

        # the player moves by "dist" from their current position, wrapping
        # around from 10 -> 1
        space = (positions[player] - 1 + dist) % 10 + 1

        # move to that position, and add that position to the score
        positions[player] = space
        scores[player] += space

        # we rolled 3 times for this player
        rolls += 3

    # the game hash (according to the problem description) is the *losing*
    # score times the number of rolls required for the game to end
    return min(scores) * rolls

def play(positions, scores, wins, player, cache):
    '''Recursively play all possible rolls from the given
       positions, scores, and player. Keep track of the
       number of wins in "wins", and cache the results for the
       state (positions, scores, player) in cache. The cache stores
       the change in the number of wins for both players, starting
       from this state.'''

    # base case: if a score has reached 21, then the previous player to play
    # must have won 1 round
    if max(scores) >= 21:
        # the winner must be the previous player to move
       #assert scores.index(max(scores)) == 1 - player
        wins[1 - player] += 1
        return

    # Memoization: have we reached this configuration before?
    # We are caching the following state; if we see it again, we can just
    # re-use the values.
    k = tuple(positions) + tuple(scores) + (player,)
    if k in cache:
        wins[player] += cache[k][player]
        wins[1-player] += cache[k][1-player]
        return

    # Since the cache stores the number of *additional* wins, we need to keep
    # track of how many wins we have now.
    orig_wins = wins[:]

    # Also save the original position and score for this player, so we can
    # easily reset later.
    orig_position = positions[player]
    orig_score = scores[player]

    # Try all possible trios of dice rolls, with a die that can roll 1, 2, or 3.
    for r1 in range(1, 4):
        for r2 in range(1, 4):
            for r3 in range(1, 4):
                # this is the space that the player lands on; it's also their
                # additional score
                space = (orig_position - 1 + r1 + r2 + r3) % 10 + 1

                positions[player] = space
                scores[player] += space

                # recurse
                play(positions, scores, wins, 1 - player, cache)

                # reset the score
                scores[player] = orig_score

    # reset the position
    positions[player] = orig_position

    # cache the change in wins for both players
    cache[k] = [wins[p] - orig_wins[p] for p in [0, 1]]

def part2(lines):
    '''The die is now 3-sided and "splits" the world into three on
       each roll. Count the number of wins for the player that wins
       the most, in all possible games. Use memoization to cache
       the results of partial games and re-use them when we see
       them again.'''
    positions = [int(line.split()[-1]) for line in lines]
    wins = [0, 0]
    play(positions, [0, 0], wins, 0, {})
    return max(wins)

if __name__ == '__main__':
    fname = '21.in'
    if len(sys.argv) > 1:
        fname = sys.argv[1]

    with open(fname) as f:
        lines = list(map(str.strip, f))

    print('part1:', part1(lines))
    print('part2:', part2(lines))

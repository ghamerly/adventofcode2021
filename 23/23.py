#!/usr/bin/env python3

# https://adventofcode.com/2021/day/23 - "amphipod"
# Author: Greg Hamerly

# This is the second attempt, using branch-and-bound search instead of Dijkstra.
# It's simpler and faster and much more memory-efficient. But it's still slow.
# Solving part 1 takes about 5 minutes, part 2 about 20 minutes (both with
# pypy3).

import sys

############# Part 1
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########

############# Numbering of cells (mod 10)
#01234567890#
###1#2#3#4###
  #3#4#5#6#
  #########

############# Part 2
#...........#
###B#C#B#D###
  #D#C#B#A# << new for part 2
  #D#B#A#C# << new for part 2
  #A#D#C#A#
  #########

############# Numbering of cells (mod 10)
#01234567890#
###1#2#3#4###
  #5#6#7#8# << new D C B A
  #9#0#1#2# << new D B A C
  #3#4#5#6#
  #########

PART1_GOAL_POSITIONS = [-1] * 11 + [0, 1, 2, 3] * 2
PART2_GOAL_POSITIONS = [-1] * 11 + [0, 1, 2, 3] * 4
PLAYER_COSTS = (1, 10, 100, 1000)

def parse(lines):
    oneline = ''.join(lines).replace('#', '')
    positions = [-1] * 19
    for i, c in enumerate('ABCD'):
        positions[oneline.index(c)] = i
        positions[oneline.rindex(c)] = i

    print('positions', positions)
    return positions

PART1_NEIGHBORS = {
        0: (1,),
        1: (0, 2),
        2: (1, 3, 11),
        3: (2, 4),
        4: (3, 5, 12),
        5: (4, 6),
        6: (5, 7, 13),
        7: (6, 8),
        8: (7, 9, 14),
        9: (8, 10),
        10: (9,),
        11: (2, 15),
        12: (4, 16),
        13: (6, 17),
        14: (8, 18),
        15: (11,),
        16: (12,),
        17: (13,),
        18: (14,),
        }

PART2_NEIGHBORS = {
        0: (1,),
        1: (0, 2),
        2: (1, 3, 11),
        3: (2, 4),
        4: (3, 5, 12),
        5: (4, 6),
        6: (5, 7, 13),
        7: (6, 8),
        8: (7, 9, 14),
        9: (8, 10),
        10: (9,),
        11: (2, 15),
        12: (4, 16),
        13: (6, 17),
        14: (8, 18),
        15: (11,19),
        16: (12,20),
        17: (13,21),
        18: (14,22),
        19: (15,23),
        20: (16,24),
        21: (17,25),
        22: (18,26),
        23: (19,),
        24: (20,),
        25: (21,),
        26: (22,),
        }

# (source, dest) -> path
PATHS = {}
DISTANCE = {}

def dfs(src, current, path):
    if current in path:
        return

    if path and current == src:
        return

    path.append(current)

    PATHS[(src,current)] = path[:]
    DISTANCE[(src,current)] = len(path)

    for neighbor in NEIGHBORS[current]:
        dfs(src, neighbor, path)

    path.pop()

def compute_paths_distances():
    global PATHS, DISTANCE, NEIGHBORS
    PATHS = {}
    DISTANCE = {}
    for src in NEIGHBORS:
        for neighbor in NEIGHBORS[src]:
            dfs(src, neighbor, [])

PART1_HOME_POSITIONS = [[11, 15],
                        [12, 16],
                        [13, 17],
                        [14, 18]]

PART2_HOME_POSITIONS = [[11, 15, 19, 23],
                        [12, 16, 20, 24],
                        [13, 17, 21, 25],
                        [14, 18, 22, 26]]

def in_hallway(pos):
    return pos <= 10

def clear_path(src, dest, positions):
    return all(positions[p] < 0 for p in PATHS[(src, dest)])

def home_ready(positions, player):
    i = len(HOME_POSITIONS[player]) - 1
    while i >= 0:
        p = HOME_POSITIONS[player][i]
        if positions[p] >= 0 and positions[p] != player:
            return False
        i -= 1
    return True

def in_final_position(positions, pos):
    player = positions[pos]
    i = len(HOME_POSITIONS[player]) - 1
    while i >= 0:
        p = HOME_POSITIONS[player][i]
        if p == pos:
            return True
        if positions[p] != player:
            return False
        i -= 1
    return False

def home_pos(player, positions):
    i = len(HOME_POSITIONS[player]) - 1
    while i >= 0:
        if positions[HOME_POSITIONS[player][i]] == -1:
            return HOME_POSITIONS[player][i]
        i -= 1
    assert False

def search(players, positions, best, dist):
    if dist >= best[0]:
        return

    if positions == GOAL_POSITIONS:
        if dist < best[0]:
            print(f'found new best: {dist} < {best[0]}')
            best[0] = dist
        return

    # speed this up by removing the players that are in final position
    for player_ndx in range(len(players)):
        player, pos = players[player_ndx]

        if in_final_position(positions, pos):
            continue

        if in_hallway(pos):
            if not home_ready(positions, player):
                continue

            home = home_pos(player, positions)
            if not clear_path(pos, home, positions):
                continue

            # move home
            positions[pos], positions[home] = positions[home], positions[pos]
            players[player_ndx][1] = home
            cost = DISTANCE[(pos,home)] * PLAYER_COSTS[player]
            search(players, positions, best, dist + cost)
            positions[pos], positions[home] = positions[home], positions[pos]
            players[player_ndx][1] = pos
        else:
            for hall_pos in [0, 1, 3, 5, 7, 9, 10]:
                if not clear_path(pos, hall_pos, positions):
                    continue

                # move to the hallway
                positions[pos], positions[hall_pos] = positions[hall_pos], positions[pos]
                players[player_ndx][1] = hall_pos
                cost = DISTANCE[(pos,hall_pos)] * PLAYER_COSTS[player]
                search(players, positions, best, dist + cost)
                positions[pos], positions[hall_pos] = positions[hall_pos], positions[pos]
                players[player_ndx][1] = pos

def solve(positions):
    players = []
    for pos, player in enumerate(positions):
        if player >= 0:
            players.append([player, pos])

    remove = []
    for i, (player, pos) in enumerate(players):
        if in_final_position(positions, pos):
            remove.append(i)

    players = [[player, pos] for i, (player, pos) in enumerate(players) if i not in remove]
    players.sort(key=lambda player_pos: PLAYER_COSTS[player_pos[0]], reverse=True)

    best = [1e100]
    search(players, positions, best, 0)

    return best[0]

def part1(positions):
    global GOAL_POSITIONS, NEIGHBORS, HOME_POSITIONS
    GOAL_POSITIONS = PART1_GOAL_POSITIONS
    NEIGHBORS = PART1_NEIGHBORS
    HOME_POSITIONS = PART1_HOME_POSITIONS
    compute_paths_distances()
    return solve(positions)

def part2(positions):
    global GOAL_POSITIONS, NEIGHBORS, HOME_POSITIONS
    GOAL_POSITIONS = PART2_GOAL_POSITIONS
    NEIGHBORS = PART2_NEIGHBORS
    HOME_POSITIONS = PART2_HOME_POSITIONS
    compute_paths_distances()

    # modification for part2
    positions_part2 = positions[:15] + [3, 2, 1, 0, 3, 1, 0, 2] + positions[15:]
    return solve(positions_part2)

# Yuck, global variables that change depending on the task
GOAL_POSITIONS = None
NEIGHBORS = None
HOME_POSITIONS = None

def main():
    regular_input = __file__.split('/')[-1][:-len('.py')] + '.in'
    file = regular_input if len(sys.argv) <= 1 else sys.argv[1]
    print(f'using input: {file}')
    with open(file) as f:
        lines = list(map(str.strip, f))

    positions_part1 = parse(lines)

    print('part 1:', part1(positions_part1))
    print('part 2:', part2(positions_part1))

if __name__ == '__main__':
    main()

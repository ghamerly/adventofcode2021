#!/usr/bin/env python3

# https://adventofcode.com/2021/day/23
# Author: Greg Hamerly

# I spent way too much time on this trying to get Dijkstra's to work. There are
# just too many states to attempt a non-bounded breadth-type of search. It takes
# forever. So: this attempt fails, but perhaps there's a way to make it fast
# enough by adding better bounds or exploiting properties of the problem (e.g.
# max 2 moves per piece).

import heapq
import sys

#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########

#############
#01234567890#
###1#2#3#4###
  #5#6#7#8#
  #########

FIRST_MOVE = 1 << 2
SECOND_MOVE = 1 << 3

NO_MOVES = 0
ONE_MOVE = FIRST_MOVE
TWO_MOVES = FIRST_MOVE | SECOND_MOVE

PLAYER_MASK = 3
MOVE_MASK = TWO_MOVES

GOAL_POSITIONS = (-1,) * 11 + tuple((i | TWO_MOVES) for i in (0, 1, 2, 3) * 2)

PLAYER_COSTS = (1, 10, 100, 1000)

# manually construct the map of neighbors that we can use to walk through the
# game
NEIGHBORS = {
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

# these are the first moves that are possible (from -> to)
FIRST_MOVES = (0, 1, 3, 5, 7, 9, 10)

# these are the second moves that are possible, sorted by player (0...3)
SECOND_MOVES = {i: (11 + i, 15 + i) for i in range(4)}

print('GOAL_POSITIONS', GOAL_POSITIONS)
print('NEIGHBORS', NEIGHBORS)
print('FIRST_MOVES', FIRST_MOVES)
print('SECOND_MOVES', SECOND_MOVES)

class GameState:
    def __init__(self, positions=[], cost=0):
        self.encoding = self.encode(positions)
        self.lower_bound = GameState.lower_bound(positions)
        self.cost = cost

    @staticmethod
    def encode(positions):
        e = 0
        NONE = 16
        for p in positions:
            if p == -1:
                p = NONE
            e = (e << 5) | p
        return e

    def decode(self):
        positions = [-1] * 19
        MASK = 31
        NONE = 16
        e = self.encoding
        for i in range(19):
            p = e & MASK
            if p == NONE:
                p = -1
            positions[18 - i] = p
            e >>= 5
        return positions

    def is_goal(self):
        #return self.positions == GOAL_POSITIONS
        return self.encoding == GOAL_ENCODING

    def search(self, positions, position, destinations, seen=None, length=0):
        seen = seen or set()
        if position in seen:
            return

        seen.add(position)

        if position in destinations:
            yield position, length

        for neighbor in NEIGHBORS[position]:
            #assert 0 <= neighbor < len(self.positions), neighbor
            if positions[neighbor] < 0:
                yield from self.search(positions, neighbor, destinations, seen, length + 1)

    def neighbors(self):
        positions = self.decode()
        for i, p in enumerate(positions):
            if p < 0 or (p & MOVE_MASK) == TWO_MOVES:
                continue

            player = p & PLAYER_MASK

            which_move = p & MOVE_MASK
            if which_move == NO_MOVES:
                destinations = FIRST_MOVES
                next_p = p | FIRST_MOVE
            else:
                assert which_move != TWO_MOVES
                destinations = SECOND_MOVES[player]
                next_p = p | SECOND_MOVE

            for position, length in self.search(positions, i, destinations):
                positions[i] = -1
                positions[position] = next_p
                #print(f'moving {p & PLAYER_MASK} from {i} to {position} with cost {cost}')
                if not GameState.stuck(positions):
                    cost = length * PLAYER_COSTS[player]
                    yield GameState(positions, self.cost + cost)
                positions[i] = p
                positions[position] = -1

    def __lt__(self, other):
        if self.cost == other.cost:
            return self.lower_bound < other.lower_bound
        return self.cost < other.cost

    def __hash__(self):
        return hash(self.encoding)

    def __repr__(self):
        return f'{self.cost}: {self.encoding}'

    @staticmethod
    def stuck(positions):
        # check to see if we are blocking ourselves
        for i in range(4):
            v = i | TWO_MOVES
            if positions[i + 11] == v and positions[i + 15] != v:
                return True

        # check to see if there is a block in the hallway
        predecessors = { 5: [3], 7: [3, 5], }
        for j in [5, 7]:
            if positions[j] < 0:
                continue
            pj = positions[j] & PLAYER_MASK
            for i in predecessors[j]:
                if positions[i] < 0:
                    continue
                if pj < (positions[i] & PLAYER_MASK):
                    return True

        return False

    @staticmethod
    def lower_bound(positions):
        distances = [
                { 0: 3, 1: 2, 3: 2, 5: 4, 7: 6, 9: 8, 10: 9,
                    11: 0, 12: 4, 13: 6, 14: 8,
                    15: 0, 16: 5, 17: 7, 18: 9 },
                { 0: 5, 1: 4, 3: 2, 5: 2, 7: 4, 9: 6, 10: 7,
                    11: 4, 12: 0, 13: 4, 14: 6,
                    15: 5, 16: 0, 17: 5, 18: 7 },
                { 0: 7, 1: 6, 3: 4, 5: 2, 7: 2, 9: 4, 10: 5,
                    11: 6, 12: 4, 13: 0, 14: 4,
                    15: 7, 16: 5, 17: 0, 18: 5 },
                { 0: 9, 1: 8, 3: 6, 5: 4, 7: 2, 9: 2, 10: 3,
                    11: 8, 12: 6, 13: 4, 14: 0,
                    15: 9, 16: 7, 17: 5, 18: 0 }
                ]
        b = 0
        for i, p in enumerate(positions):
            if p < 0:
                continue
            player = p & PLAYER_MASK
            b += distances[player][i] * PLAYER_COSTS[player]

        return b

    def display(self):
        m = {i: (1, i+1) for i in range(11)}
        m.update({i + 11: (2, 2 * i + 3) for i in range(4)})
        m.update({i + 15: (3, 2 * i + 3) for i in range(4)})

        board = [
                list('#############'),
                list('#...........#'),
                list('###.#.#.#.###'),
                list('  #.#.#.#.#'),
                list('  #########')
        ]

        letters = {
                0: 'a', (0 | ONE_MOVE): 'A', (0 | TWO_MOVES): 'å',
                1: 'b', (1 | ONE_MOVE): 'B', (1 | TWO_MOVES): '∫',
                2: 'c', (2 | ONE_MOVE): 'C', (2 | TWO_MOVES): 'ç',
                3: 'd', (3 | ONE_MOVE): 'D', (3 | TWO_MOVES): '∂'
                }

        positions = self.decode()

        for i, p in enumerate(positions):
            if p < 0:
                continue
            row, col = m[i]
            board[row][col] = letters[p]

        print(self.cost)
        for row in board:
            print(''.join(row))

    @staticmethod
    def parse(lines):
        oneline = ''.join(lines).replace('#', '')
        positions = [-1] * 19
        for i, c in enumerate('ABCD'):
            positions[oneline.index(c)] = i
            positions[oneline.rindex(c)] = i

        # we don't need to move if the tokens are already in position
        for i in range(4):
            if positions[i + 15] == i:
                positions[i + 15] = i | TWO_MOVES
                if positions[i + 11] == i:
                    positions[i + 11] = i | TWO_MOVES

        return GameState(positions)

GOAL_ENCODING = GameState.encode(GOAL_POSITIONS)

def part1(s):
    frontier = [s]

    cost = {s: 0}

    oo = 1e100

    i = 0
    while frontier:
        i += 1
        s = heapq.heappop(frontier)

        if i % 1000 == 0:
            print(i, len(frontier))
            s.display()

        for neighbor in s.neighbors():
            if neighbor.cost <= cost.get(neighbor, oo):
                cost[neighbor] = neighbor.cost
                heapq.heappush(frontier, neighbor)
            # technically, we should only return once we pull it out of the
            # frontier
            if neighbor.is_goal():
                print('found it')
                neighbor.display()
                return neighbor.cost

def part2(lines):
    pass

def main():
    regular_input = __file__.split('/')[-1][:-len('.py')] + '.in'
    file = regular_input if len(sys.argv) <= 1 else sys.argv[1]
    print(f'using input: {file}')
    with open(file) as f:
        lines = list(map(str.strip, f))

    s = GameState.parse(lines)

    print('part 1:', part1(s))
    print('part 2:', part2(lines))

if __name__ == '__main__':
    main()

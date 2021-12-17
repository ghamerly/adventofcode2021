#!/usr/bin/env python3

# https://adventofcode.com/2021/day/17 - "trick shot"
# Author: Greg Hamerly

# I'm not proud of this code. It's brute-force, with bounds chosen based on
# guess-and-check. I didn't have a chance to do my usual cleanup after solving.
# Things I can think of to do to improve, if I had time:
#   - if using brute-force, detect the proper bounds (including
#     positive/negative values)
#   - derive closed-form solutions, or at least binary search

import sys

def part1(xrange, yrange):
    '''Search over y velocities; for each velocity, determine if there is some x
    velocity that can hit the target. Take the maximum y velocity that works,
    and then solve for the height it reaches (which is the identity
    n(n+1)/2, if n is the y velocity).'''

    def can_hit(y_vel):
        '''Determine if it is possible (True/False) if the given y velocity can
        be made to hit the target. It's not possible if:
            - the y coordinate misses the target, or
            - there is no x velocity that works to hit the target.
        We assume that max(yrange) < 0, which is terrible.
            '''

        y = 0
        vel = y_vel
        steps = 0
        while yrange[1] < y:
            steps += 1
            y += vel
            vel -= 1

        if y < yrange[0]:
            return False # we overstepped the target

        # search for the x velocity that is at most "steps", since otherwise our
        # first step would overshoot; assume x_vel >= 0.
        for x_vel in range(steps + 1):
            dist = x_vel * (x_vel - 1) // 2
            if xrange[0] <= dist <= xrange[1]:
                return True

        # we never hit the target
        return False

    # find the largest y velocity that hits the target
    max_y_vel = max(filter(can_hit, range(1000)))

    # the highest point is given by n(n+1)/2, since we add up the decreasing
    # velocities
    return max_y_vel * (max_y_vel + 1) // 2

def part2(xrange, yrange):
    '''Search over all possible pairs of velocities (within a reasonable range)
    and see which of them hit the target, by brute-force simulation.'''

    # check our assumptions... our code isn't general enough
    assert min(xrange) > 0
    assert max(yrange) < 0

    def can_hit(x_vel, y_vel):
        '''Just brute-force simulation of the given velocities.'''
        assert x_vel >= 0
        x = y = 0
        for _ in range(1000): # simulate at most this many steps
            x, y = x + x_vel, y + y_vel

            if xrange[0] <= x <= xrange[1] and yrange[0] <= y <= yrange[1]:
                return True

            # update the velocities according to the rules given in the problem
            y_vel -= 1
            x_vel = max(x_vel - 1, 0) # assume x_vel >= 0

            # overshoot detection -- saves a lot of time
            if y < min(yrange) or max(xrange) < x:
                return False

        return False

    # Just sum up the velocity pairs that hit the target.
    # We assume the x velocity is non-negative -- i.e. the target is in front of
    # us.
    return sum(can_hit(xv, yv) for xv in range(500) for yv in range(-350, 500))

def main():
    regular_input = __file__.split('/')[-1][:-len('.py')] + '.in'
    file = regular_input if len(sys.argv) <= 1 else sys.argv[1]
    print(f'using input: {file}')
    with open(file) as f:
        lines = list(map(str.strip, f))

    tokens = lines[0].split()
    xrange = list(map(int, tokens[2][2:-1].split('..')))
    yrange = list(map(int, tokens[3][2:].split('..')))

    print('part 1:', part1(xrange, yrange))
    print('part 2:', part2(xrange, yrange))

if __name__ == '__main__':
    main()

#!/usr/bin/env python3

# https://adventofcode.com/2021/day/20 - "trench map"
# Author: Greg Hamerly

# This fooled me into thinking it is an easy problem... until I realized that
# dealing with "program[0] = '#'" (i.e. all bits everywhere get turned on every
# other iteration step) was possible. I'm guessing many people had that feeling.
#
# Getting the right abstraction to deal with the infinite bits being on was
# somewhat tricky (well, finding it was). The key for me was realizing that the
# original image always grows by one row/column in each direction each
# iteration, so I can keep track of those bounds and know where "infinity"
# begins -- and use an "infinite" bit to represent beyond that.

import sys

class Image:
    '''An image holds bits that are turned on, plus whether the bits that are
    infinitely far away are turned on. It also keeps track of the bounds, which
    grow by 1 row/col each time we augment the image.'''

    def __init__(self, lines=None, infinite=False):
        '''Parse the given sequence of lines (list of strings) and build the
        initial image; also take on the value of the infinite bit.'''
        lines = lines or []
        self.image = set()
        for r, line in enumerate(lines):
            for c, char in enumerate(line):
                if char == '#':
                    self.image.add((r, c))

        # infinite represents the value of bits that are outside the image
        # bounds
        self.infinite = infinite

        # bounds keeps track of the extents of the image
        self.bounds = [0, 0, 0, 0]
        if lines:
            self.bounds = [0, len(lines), 0, len(lines[0])]

    def get_bit(self, r, c):
        '''Get the value of the bit at (r,c). If that is outside the range we
        care about, then return the infinite bit.'''
        rmin, rmax, cmin, cmax = self.bounds
        if rmin <= r <= rmax and cmin <= c <= cmax:
            return (r, c) in self.image
        return self.infinite

    def display(self):
        '''Render the current image as a grid, plus a little on each side. Also
        add row/column numbers (mod 10) to help compare images.'''
        out = []
        bit = lambda r, c: '.#'[self.get_bit(r, c)]
        rmin, rmax, cmin, cmax = self.bounds
        print('  ' + ''.join(f'{c%10}' for c in range(cmin-3, cmax+4)))
        for r in range(rmin-3, rmax+4):
            n = f'{r%10:<2}'
            out.append(n + ''.join(bit(r,c) for c in range(cmin-3, cmax+4)))
        print('\n'.join(out))

    def apply(self, program):
        '''Apply the program to this Image, and return the result.'''

        # the next Image has infinite = True if infinite is currently false, and
        # program[0] == '#'
        new_image = Image(infinite=(not self.infinite) and (program[0] == '#'))

        rmin, rmax, cmin, cmax = self.bounds

        # grow by one row/col in each direction
        new_image.bounds = [rmin - 1, rmax + 1, cmin - 1, cmax + 1]

        for r in range(rmin - 1, rmax + 2):
            for c in range(cmin - 1, cmax + 2):
                index = 0
                for rr in range(r-1,r+2):
                    for cc in range(c-1,c+2):
                        index = (index << 1) | self.get_bit(rr, cc)
                if program[index] == '#':
                    new_image.image.add((r,c))

        return new_image

def iterate_program(program, image, num_iters, display=False):
    '''Apply the given program to the image, num_iters times. Optionally display
    each step.'''
    for i in range(num_iters):
        if display:
            print('-' * 10, i, image.infinite, len(image.image))
            image.display()
        image = image.apply(program)

    if display:
        print('final')
        print('-' * 10, i, image.infinite, len(image.image))
        image.display()

    return len(image.image)


def part1(program, image):
    '''How many bits are turned on after 2 iterations?'''
    return iterate_program(program, image, 2, False)

def part2(program, image):
    '''How many bits are turned on after 50 iterations?'''
    return iterate_program(program, image, 50, False)

def main():
    regular_input = __file__.split('/')[-1][:-len('.py')] + '.in'
    file = regular_input if len(sys.argv) <= 1 else sys.argv[1]
    print(f'using input: {file}')
    with open(file) as f:
        lines = list(map(str.strip, f))

    program = lines[0]
    image = Image(lines[2:])

    # we're mapping an infinite set of bits; if both program[0] and program[511]
    # are on, then they flip on and stay on. We cannot count this many
    # (infinity), so assert that's not the case.
    assert program[0] == '.' or program[-1] == '.'

    print('part 1:', part1(program, image))
    print('part 2:', part2(program, image))

if __name__ == '__main__':
    main()

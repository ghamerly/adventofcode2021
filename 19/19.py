#!/usr/bin/env python3

# https://adventofcode.com/2021/day/19 - "beacon scanner"
# Author: Greg Hamerly

import sys

class Point:
    def __init__(self, x, y, z):
        self.coords = (x, y, z)

    def cross(self, other):
        '''The cross product between two 3d vectors.'''
        a = self.coords
        b = other.coords

        s0 = a[1] * b[2] - a[2] * b[1]
        s1 = a[2] * b[0] - a[0] * b[2]
        s2 = a[0] * b[1] - a[1] * b[0]

        return Point(s0, s1, s2)

    def __sub__(self, other):
        '''The vector of (self - other).'''
        x1, y1, z1 = self.coords
        x2, y2, z2 = other.coords
        return Point(x1 - x2, y1 - y2, z1 - z2)

    def __add__(self, other):
        '''The vector of (self + other).'''
        x1, y1, z1 = self.coords
        x2, y2, z2 = other.coords
        return Point(x1 + x2, y1 + y2, z1 + z2)

    def __eq__(self, other):
        return self.coords == other.coords

    def __ne__(self, other):
        return self.coords != other.coords

    def rotate(self, rotation):
        '''Rotate according to the given rotation. The rotation encodes a tuple
        of the indexes and signs of each of the coordinates.'''
        f_ndx, f_sgn, u_ndx, u_sgn, o_ndx, o_sgn = rotation
        c = [0] * 3
        c[f_ndx] = self.coords[0] * f_sgn
        c[u_ndx] = self.coords[1] * u_sgn
        c[o_ndx] = self.coords[2] * o_sgn
        return Point(*c)

    def __hash__(self):
        return hash(self.coords)

    def __repr__(self):
        return ','.join(map(str, self.coords))

def gen_rotations():
    '''Generate data on the 24 canonical rotations... using cross products to
    figure out which direction the third coordinate is pointing.'''

    # create the 6 canonical direction vectors, and remember which coordinate is
    # non-zero
    units = []
    for x in [1, -1]:
        units.append((0, Point(x, 0, 0)))
        units.append((1, Point(0, x, 0)))
        units.append((2, Point(0, 0, x)))

    # Now try all combinations of cross products of pairs of the unit vectors
    # created above. Keep only those that have a non-zero cross-product.
    rotations = []
    for facing_ndx, facing in units:
        for up_ndx, up in units:

            # find the sign of the other coordinate using the cross-product
            other = facing.cross(up)
            if not any(other.coords):
                continue

            # the three coordinates (0, 1, or 2) always sum to 3, so the
            # missing one can be computed by subtracting the first two from 3.
            other_ndx = 3 - facing_ndx - up_ndx

            # record the index and sign of each coordinate of this rotation
            rotations.append((
                facing_ndx, facing.coords[facing_ndx],
                up_ndx, up.coords[up_ndx],
                other_ndx, other.coords[other_ndx]
                ))

    return rotations

class Scanner:
    def __init__(self, beacons):
        self.beacons = beacons

    def rotate(self, rotation):
        return Scanner([b.rotate(rotation) for b in self.beacons])

    def __repr__(self):
        return f'{len(self.beacons)}: {self.beacons}'

    def find_mapping(self, other):
        '''Try to match each beacon with each other beacon. Use that as an
        offset, and see if applying that offset to each beacon leads to a
        consistent matching.'''

        self_beacons = set(self.beacons)
        for b1 in self.beacons:
            for b2 in other.beacons:
                # the offset needed to map b2 -> b1
                offset = b1 - b2

                # apply this offset to all the beacons in "other"
                mapped_beacons = [b3 + offset for b3 in other.beacons]

                # according to the problem, there's a match if at least 12
                # points overlap between two scanners
                if len(set(mapped_beacons) & self_beacons) >= 12:
                    return mapped_beacons, offset

        return None

def merge_scanners(scanners, rotations):
    '''Start with the first scanner, and repeatedly try to add other scanners by
    finding a rotation that maps them into the first scanner's space. If we find
    a match, then add those points (but eliminate duplicates).'''

    # s is the scanner we merge everything else into
    s = scanners[0]
    # these scanners have yet to be merged
    scanners_left = list(range(1, len(scanners)))
    # record the offsets of each scanner
    scanner_positions = {0: Point(0, 0, 0)}
    while scanners_left:
        #print('scanners_left', scanners_left)
        scanners_remaining = []
        for s2_ndx in scanners_left:
            for rotation in rotations:
                s2_rot = scanners[s2_ndx].rotate(rotation)
                result = s.find_mapping(s2_rot)
                if result:
                    mapped_beacons, offset = result
                    #print(f'joining {s2_ndx} with {rotation}')
                    # join the beacons, eliminating duplicates
                    s.beacons = list(set(s.beacons + mapped_beacons))
                    scanner_positions[s2_ndx] = offset
                    break
            else:
                # if we weren't able to merge s2_ndx, keep it for later
                scanners_remaining.append(s2_ndx)
        scanners_left = scanners_remaining

    return s.beacons, scanner_positions

def part1(beacons, scanner_positions):
    '''Return the number of beacons left after merging all scanners.'''
    return len(beacons)

def part2(beacons, scanner_positions):
    '''Find the maximum Manhattan distance between any pair of scanners.'''
    dist = 0
    for s1 in scanner_positions.values():
        for s2 in scanner_positions.values():
            dist = max(dist, sum(map(abs, (s1 - s2).coords)))
    return dist

def parse(lines):
    # scanner_id => observations, assuming scanners come in increasing numeric
    # ID order starting at 0
    scanners = []
    for line in lines:
        if not line:
            continue
        if line.startswith('---'):
            scanner_id = int(line.split()[2])
            assert scanner_id == len(scanners)
            scanners.append(Scanner([]))
            continue
        x, y, z = map(int, line.split(','))
        scanners[-1].beacons.append(Point(x, y, z))

    return scanners

def main():
    regular_input = __file__.split('/')[-1][:-len('.py')] + '.in'
    file = regular_input if len(sys.argv) <= 1 else sys.argv[1]
    print(f'using input: {file}')
    with open(file) as f:
        lines = list(map(str.strip, f))

    scanner_data = parse(lines)
    rotations = gen_rotations()

    beacons, scanner_positions = merge_scanners(scanner_data, rotations)

    print('part 1:', part1(beacons, scanner_positions))
    print('part 2:', part2(beacons, scanner_positions))

if __name__ == '__main__':
    main()

#!/usr/bin/env python3

# https://adventofcode.com/2021/day/22 - "reactor reboot"
# Author: Greg Hamerly

# I lost a lot of sleep on this. But I enjoyed incrementally improving my
# program from taking an hour to run to just a few minutes. However, I still
# feel like I'm missing a key element that would make the program run faster. I
# stopped after not being able to get a reduction algorithm to work that was
# based on hashing the face areas of the cubes.
#
# Also, everywhere it says "cube", it should really say "cuboid."

import collections
import sys
import re

def overlapping_range(alow, ahigh, blow, bhigh):
    '''Return true if the two ranges overlap. Touching is
    considered overlapping.'''
    return alow <= blow <= ahigh or blow <= alow <= bhigh

def size(r):
    '''Return the size of a range.'''
    return (r[1] - r[0]) + 1

class Cube:
    def __init__(self, xr, yr, zr):
        for r in [xr, yr, zr]:
            assert r[0] <= r[1]

        self.xrange = xr
        self.yrange = yr
        self.zrange = zr

    def __eq__(self, other):
        return self.xrange == other.xrange and \
                self.yrange == other.yrange and \
                self.zrange == other.zrange

    def __ne__(self, other):
        return not (self == other)

    def tuple(self):
        return (self.xrange, self.yrange, self.zrange)

    def __lt__(self, other):
        return self.tuple() < other.tuple()

    def __hash__(self):
        return hash(self.xrange + self.yrange + self.zrange)

    def overlaps(self, other):
        return overlapping_range(*(self.xrange + other.xrange)) and \
               overlapping_range(*(self.yrange + other.yrange)) and \
               overlapping_range(*(self.zrange + other.zrange))

    def xarea(self): return size(self.yrange) * size(self.zrange)
    def yarea(self): return size(self.xrange) * size(self.zrange)
    def zarea(self): return size(self.xrange) * size(self.yrange)

    def volume(self):
        return size(self.xrange) * size(self.yrange) * size(self.zrange)

    def can_join(self, other):
        '''Return true if the two cubes are exactly touching on one face (x, y,
        or z). For this to be true, they must have two of the three ranges be
        the same, and be 1 apart in the other range.'''
        match_x = self.xrange == other.xrange
        match_y = self.yrange == other.yrange
        match_z = self.zrange == other.zrange
        touching_x = (self.xrange[1] + 1 == other.xrange[0]) or (other.xrange[1] + 1 == self.xrange[0])
        touching_y = (self.yrange[1] + 1 == other.yrange[0]) or (other.yrange[1] + 1 == self.yrange[0])
        touching_z = (self.zrange[1] + 1 == other.zrange[0]) or (other.zrange[1] + 1 == self.zrange[0])

        return (match_x and match_y and touching_z) or \
                (match_x and match_z and touching_y) or \
                (match_y and match_z and touching_x)

    def join(self, other):
        '''Here, we are assuming that at least two of the three dimensions
        overlap (so that the two cubes are touching on one entire face). That
        is, this method should only be called if self.can_join(other) is
        true.'''

        minmax = lambda l: (min(l), max(l))

        xrange = minmax(self.xrange + other.xrange)
        yrange = minmax(self.yrange + other.yrange)
        zrange = minmax(self.zrange + other.zrange)

        return Cube(xrange, yrange, zrange)

    def intersect(self, other):
        '''Iteratively yield the 27 sub-cubes for intersecting self with
        other.'''
        assert self.overlaps(other)

        # There are 27 possible cubes that result from intersecting two cubes.
        # Here are the 9 regions in the set of possible intersections of two
        # rectangles in 2d:
        #   
        #   +---+-----+---+
        #   | 0 |  1  | 2 |
        #   +---+-----+---+
        #   |   |     |   |
        #   | 3 |  4  | 5 |
        #   |   |     |   |
        #   +---+-----+---+
        #   | 6 |  7  | 8 |
        #   +---+-----+---+
        #
        # and in 3d, there are three layers of these.

        xr = sorted([(self.xrange[0], 0), (self.xrange[1], 1), (other.xrange[0], 0), (other.xrange[1], 1)])
        yr = sorted([(self.yrange[0], 0), (self.yrange[1], 1), (other.yrange[0], 0), (other.yrange[1], 1)])
        zr = sorted([(self.zrange[0], 0), (self.zrange[1], 1), (other.zrange[0], 0), (other.zrange[1], 1)])

        for i in range(3):
            (xlow, xlow_end), (xhigh, xhigh_end) = xr[i], xr[i+1]
            if xlow_end: xlow += 1
            if not xhigh_end: xhigh -= 1
            if not xlow <= xhigh:
                continue

            for j in range(3):
                (ylow, ylow_end), (yhigh, yhigh_end) = yr[j], yr[j+1]
                if ylow_end: ylow += 1
                if not yhigh_end: yhigh -= 1
                if not ylow <= yhigh:
                    continue
                for k in range(3):
                    (zlow, zlow_end), (zhigh, zhigh_end) = zr[k], zr[k+1]
                    if zlow_end: zlow += 1
                    if not zhigh_end: zhigh -= 1
                    if zlow <= zhigh:
                        # just yield all of them
                        yield Cube((xlow, xhigh), (ylow, yhigh), (zlow, zhigh))

    def __repr__(self):
        return f'{self.xrange},{self.yrange},{self.zrange}'

    def part1_range(self):
        '''Determine if the cube is in the range specified by the problem for
        part 1. Only applies to part 1 of today's challenge.'''
        for r in [self.xrange, self.yrange, self.zrange]:
            a, b = r
            if a < -50 or a > 50 or b < -50 or b > 50:
                return False
        return True

    def range(self):
        '''Iteratively yield integers that uniquely represent the points in the
        cuboid bounded by +/-50 in all directions. Only applies to part 1 of
        today's challenge.'''
        for x in range(self.xrange[0], self.xrange[1] + 1):
            xx = x * 100 * 100
            for y in range(self.yrange[0], self.yrange[1] + 1):
                xy = xx + y * 100
                for z in range(self.zrange[0], self.zrange[1] + 1):
                    yield xy + z

# for parsing
rp='-?[0-9]+[.][.]-?[0-9]+'
pattern = re.compile(f'^(?P<cmd>(on|off)) x=(?P<xr>{rp}),y=(?P<yr>{rp}),z=(?P<zr>{rp})$')

def part1(cubes):
    cubes = [c for c in cubes if c[1].part1_range()]

    memory = set()
    for cmd, cube in cubes:
        if cmd:
            memory.update(cube.range())
        else:
            memory = memory - set(cube.range())

    return len(memory)

def any_intersect(cubes):
    for c1 in cubes:
        for c2 in cubes:
            if c1 != c2 and c1.overlaps(c2):
                return True
    return False

REDUCE_CUBES = 'noreduce' not in sys.argv

# FIXME -- this doesn't work
# The main idea is to only try to join cubes whose faces match by hashing their
# face area. I tried to do this just for x, but it kept producing overlapping
# cubes.
#def reduce_cubes_hash_area(cubes):
#    cubes_by_xface = collections.defaultdict(list)
#    #cubes_by_yface = collections.defaultdict(list)
#    #cubes_by_zface = collections.defaultdict(list)
#    for c in cubes:
#        cubes_by_xface[c.xarea()].append(c)
#        #cubes_by_yface[c.yarea()].append(c)
#        #cubes_by_zface[c.zarea()].append(c)
#
#    last_cubes = -1
#    current_cubes = len(cubes)
#    while current_cubes != last_cubes:
#        last_cubes = current_cubes
#        areas = list(cubes_by_xface)
#        print(f'* all areas {areas} {current_cubes}')
#        print(f'   all cubes_by_xface: {cubes_by_xface}')
#        area_ndx = 0
#        while area_ndx < len(areas):
#            x_list = cubes_by_xface[areas[area_ndx]]
#            ensure_no_overlap(x_list)
#            ensure_no_overlap(sum(cubes_by_xface.values(), []))
#            i = 0
#            while i < len(x_list):
#                j = i + 1
#                found_join = False
#                while j < len(x_list):
#                    c1, c2 = x_list[i], x_list[j]
#                    if c1.can_join(c2):
#                        found_join = True
#                        print(f'removing {x_list[i] == c1} {x_list[j] == c2} {len(x_list)} {i} {j} {c1} {c2}')
#                        print(f'  x_list = {x_list}')
#                        x_list[i] = x_list[-1]
#                        x_list.pop()
#                        if j < len(x_list):
#                            x_list[j] = x_list[-1]
#                        x_list.pop()
#                        joined = c1.join(c2)
#                        a = joined.xarea()
#                        print(f'joining {area_ndx} {areas[area_ndx]} => {a}; {c1} {c2} => {joined}')
#                        if areas.count(a) == 0:
#                            print(f'created a new area ({a})')
#                            areas.append(a)
#                        cubes_by_xface[a].append(joined)
#                        print(f'after join: {x_list}')
#                        current_cubes -= 1
#                    else:
#                        j += 1
#
#                if not found_join:
#                    i += 1
#
#            area_ndx += 1
#
#    print(cubes_by_xface)
#    cubes = sum(cubes_by_xface.values(), [])
#    ensure_no_overlap(cubes)
#    return cubes

def reduce_cubes_brute_force(cubes):
    if not REDUCE_CUBES:
        return cubes
    '''Given some cubes, join together those cubes that can
    be joined by looking at all pairs (repeatedly).'''
    cubes_list = list(cubes)
    remaining_length = -1
    remaining = []
    old_volume = sum(c.volume() for c in cubes)

    while remaining_length != len(remaining):
        # "remaining" contains those indexes of the
        # cubes_list which are available for joining.
        remaining = list(range(len(cubes_list)))
        reduced_cubes = []
        remaining_length = len(remaining)

        i = 0
        while i < len(remaining):
            # treat the i'th remaining as the next unique
            # cube which we join other cubes to
            reduced_cubes.append(cubes_list[remaining[i]])

            # try to join everything else to the current one
            j = i + 1
            while j < len(remaining):
                c2 = cubes_list[remaining[j]]
                if reduced_cubes[-1].can_join(c2):
                    joined = reduced_cubes[-1].join(c2)
                    assert reduced_cubes[-1].volume() + c2.volume() == joined.volume()
                    reduced_cubes[-1] = joined

                    # we joined j, so remove it from remaining
                    remaining[-1], remaining[j] = remaining[j], remaining[-1]
                    remaining.pop()
                else:
                    j += 1
            i += 1

        cubes_list = reduced_cubes

    new_volume = sum(c.volume() for c in cubes_list)
    assert old_volume == new_volume, (old_volume, new_volume)

    return cubes_list

def reduce_cubes(cubes):
    if REDUCE_CUBES:
        return reduce_cubes_brute_force(cubes)
    return cubes

def part2(cubes):
    # discard any beginning cubes that are off
    first_on = 0
    while first_on < len(cubes) and not cubes[first_on][0]:
        first_on += 1

    cubes = cubes[first_on:]
    on_cubes = [cubes[0][1]]

    cube_num = 2
    for new_cmd, new_cube in cubes[1:]:
        print(cube_num, '/', len(cubes), '-' * 10)
        cube_num += 1

        if not new_cmd:
            # turn off lights
            i = 0
            new_cubes = []
            while i < len(on_cubes):
                on_cube = on_cubes[i]
                if on_cube.overlaps(new_cube):
                    on_cubes[i], on_cubes[-1] = on_cubes[-1], on_cubes[i]
                    on_cubes.pop()
                    new_cubes.extend(reduce_cubes([c for c in on_cube.intersect(new_cube) if c.overlaps(on_cube) and not c.overlaps(new_cube)]))
                else:
                    i += 1

            on_cubes.extend(new_cubes)

            print(f'after {new_cmd}, {new_cube}')
            print(f'on_cubes: {len(on_cubes)}')
            print(f'current volume: {sum([c.volume() for c in on_cubes])}')

        else:
            # turn on lights -- but avoid double counting

            # Keep a (hopefully) small frontier of cubes
            # that should be added. Repeatedly find
            # intersections with the existing cubes, and
            # split those intersections into things that
            # should go back into the original set (which
            # were guaranteed to not have any intersections
            # with anything else), or stay in the frontier
            # (which needs further comparison with other
            # pre-existing cubes).

            # Getting this to only be a triply-nested loop
            # (as opposed to quadruple or quintuple) took a
            # lot of patience and fiddling.
            frontier = [new_cube]
            i = 0
            while i < len(on_cubes):
                j = 0
                found_intersection = False
                while j < len(frontier) and i < len(on_cubes):
                    c1 = frontier[j]
                    c2 = on_cubes[i]
                    if c1.overlaps(c2):
                        found_intersection = True
                        # get rid of frontier[j] and on_cubes[i]
                        frontier[-1], frontier[j] = frontier[j], frontier[-1]
                        frontier.pop()
                        on_cubes[-1], on_cubes[i] = on_cubes[i], on_cubes[-1]
                        on_cubes.pop()

                        for c in c1.intersect(c2):
                            if c2.overlaps(c):
                                # all parts that were originally part of
                                # the on_cubes set should stay there
                                on_cubes.append(c)
                            elif c1.overlaps(c):
                                # parts that were not but are in the new
                                # cube should be added back to the frontier
                                frontier.append(c)
                    else:
                        j += 1

                if not found_intersection:
                    i += 1
            
            ensure_no_overlap(on_cubes)
            ensure_no_overlap(frontier)

            on_cubes += frontier

            print(f'after {new_cmd}, {new_cube}')
            print(f'on_cubes: {len(on_cubes)}')
            print(f'current volume: {sum([c.volume() for c in on_cubes])}')

        # sanity check
        ensure_no_overlap(on_cubes)

        # reduce on_cubes
        old_volume = sum([c.volume() for c in on_cubes])
        orig_len = len(on_cubes)
        on_cubes = reduce_cubes(on_cubes)
        print(f'reduced {orig_len} -> {len(on_cubes)}')
        new_volume = sum([c.volume() for c in on_cubes])
        assert old_volume == new_volume, (old_volume, new_volume)

        # sanity check 2
        ensure_no_overlap(on_cubes)

    return sum([c.volume() for c in on_cubes])

def ensure_no_overlap(cubes):
    for c1 in cubes:
        for c2 in cubes:
            if c1 < c2:
                assert not c1.overlaps(c2), (c1, c2)

def parse(lines):
    f = lambda r: tuple(map(int, r.split('..')))
    cubes = []
    for line in lines:
        m = pattern.match(line)
        assert m, line
        cmd = m.group('cmd') == 'on'
        xr = f(m.group('xr'))
        yr = f(m.group('yr'))
        zr = f(m.group('zr'))
        c = Cube(xr, yr, zr)

        cubes.append((cmd, c))

    return cubes

if __name__ == '__main__':
    regular_input = __file__.split('/')[-1][:-len('.py')] + '.in'
    file = regular_input if len(sys.argv) <= 1 else sys.argv[1]
    print(f'using input: {file}')
    with open(file) as f:
        lines = list(map(str.strip, f))

    cubes = parse(lines)

    print('part1:', part1(cubes))
    print('part2:', part2(cubes))

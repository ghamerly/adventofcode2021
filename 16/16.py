#!/usr/bin/env python3

# https://adventofcode.com/2021/day/16 - "packet decoder"
# Author: Greg Hamerly

import sys

# Class hierarchy:
#   Packet
#       +- Literal
#       +- Operator
#           +- Sum
#           +- Product
#           +- Minimum
#           +- Maximum
#           +- Greater
#           +- Less
#           +- Equal

class Packet:
    def __init__(self, version, type_id):
        self.version = version
        self.type_id = type_id

    def value(self):
        assert False

class Literal(Packet):
    def __init__(self, version, type_id, _val):
        super().__init__(version, type_id)
        assert type_id == 4
        self.val = _val

    def value(self):
        return self.val

    def __repr__(self):
        return f'{self.version}: {self.val}'

class Operator(Packet):
    def __init__(self, version, type_id, children):
        super().__init__(version, type_id)
        assert type_id != 4
        self.children = children

    def __repr__(self):
        return f'[{self.version}: {type(self)} {self.children}]'

class Sum(Operator):
    def value(self):
        return sum(c.value() for c in self.children)

class Product(Operator):
    def value(self):
        p = 1
        for c in self.children:
            p *= c.value()
        return p

class Minimum(Operator):
    def value(self):
        return min(c.value() for c in self.children)

class Maximum(Operator):
    def value(self):
        return max(c.value() for c in self.children)

class Greater(Operator):
    def value(self):
        return 1 if self.children[0].value() > self.children[1].value() else 0

class Less(Operator):
    def value(self):
        return 1 if self.children[0].value() < self.children[1].value() else 0

class Equal(Operator):
    def value(self):
        return 1 if self.children[0].value() == self.children[1].value() else 0

# Look up an Operator sub-type by its type_id integer value, defined in the
# problem.
OPERATOR_TYPE = {
        0: Sum,
        1: Product,
        2: Minimum,
        3: Maximum,
        5: Greater,
        6: Less,
        7: Equal
        }

def part1(packets):
    '''Add up the version numbers in all the packets, recursively.'''
    ans = 0
    for packet in packets:
        ans += packet.version
        if isinstance(packet, Operator):
            ans += part1(packet.children)
    return ans

def part2(packets):
    '''Evaluate the expression.'''
    assert len(packets) == 1
    return packets[0].value()

def parse_packets(bits, pos, packets):
    '''Parse the given bitstring (starting at index "pos") into a hierarchy of
    packets, according to the byzantine rules given in the problem. Place each
    packet into the list "packets", and return the index where parsing
    stopped.'''

    LITERAL = 4
    #print(f'parsing at {pos} (out of {len(bits)})')
    version = int(bits[pos:pos+3], 2)
    type_id = int(bits[pos+3:pos+6], 2)

    if type_id == LITERAL:
        #print(f'Found LITERAL at {pos}')
        pos += 6
        b = []
        while bits[pos] == '1':
            # take each group of 4 bits (following the '1', indicating
            # continuation)
            b.append(bits[pos+1:pos+5])
            pos += 5
        # take the last group of 4 bits (following the '0', indicating stop)
        b.append(bits[pos+1:pos+5])
        pos += 5

        packets.append(Literal(version, type_id, int(''.join(b), 2)))

        return pos

    else: # operator type
        #print(f'Found OPERATOR at {pos}')
        children = []
        if bits[pos + 6] == '0':
            # look at 15 bits for the number of sub-packet bits to parse
            length = int(bits[pos+7:pos+22], 2)
            pos += 22
            end = pos + length
            while pos < end:
                pos = parse_packets(bits, pos, children)
        else:
            # look at 11 bits for the number of sub-packets
            num_sub_packets = int(bits[pos+7:pos+18], 2)
            pos += 18
            for i in range(num_sub_packets):
                pos = parse_packets(bits, pos, children)

        packets.append(OPERATOR_TYPE[type_id](version, type_id, children))

        return pos

def parse_hex(hexstring):
    return ''.join(f'{int(h, 16):04b}' for h in hexstring)

def main():
    regular_input = __file__.split('/')[-1][:-len('.py')] + '.in'
    file = regular_input if len(sys.argv) <= 1 else sys.argv[1]
    print(f'using input: {file}')
    with open(file) as f:
        lines = list(map(str.strip, f))

    for i, line in enumerate(lines):
        print('-' * 30, i)
        print(line)
        bits = ''.join(f'{int(h, 16):04b}' for h in line)
        #print(f'bits = {bits} ({len(bits)})')
        packets = []
        parse_packets(bits, 0, packets)
        #print(packets)

        print('part 1:', part1(packets))
        print('part 2:', part2(packets))

if __name__ == '__main__':
    main()

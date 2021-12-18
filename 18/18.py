#!/usr/bin/env python3

# https://adventofcode.com/2021/day/18 - "snailfish"
# Author: Greg Hamerly

import sys
import json

class Tree:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def copy(self):
        left = self.left.copy() if self.left else None
        right = self.right.copy() if self.right else None
        return Tree(left, right)

    def add(self, right):
        '''Join this tree as a left child with another to its right.'''
        return Tree(self, right)

    def _str(self, depth):
        '''Display the tree in a way that highlights those pairs that should
        explode.'''
        a = '[' if depth < 4 else '('
        b = ']' if depth < 4 else ')'
        return f'{a}{self.left._str(depth+1)},{self.right._str(depth+1)}{b}'

    def __repr__(self):
        return self._str(0)

    def magnitude(self):
        '''Find the "magnitude" -- a checksum defined by the problem -- for this
        tree.'''
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()
            
    def explode(self):
        '''Explode the given pair, return a dictionary indicating what should
        replace, go left, and go right.'''
        assert isinstance(self.left, TreeLeaf)
        assert isinstance(self.right, TreeLeaf)
        return 'explode', {'replacement': TreeLeaf(0),
                           'left': self.left.val,
                           'right': self.right.val}

    def should_split(self):
        '''Trees that have children should never split.'''
        return False
    def should_explode(self, depth):

        '''Trees that are deep enough should explode.'''
        return depth >= 4

    def add_leftmost(self, x):
        '''Find the leftmost node, add x to it.'''
        self.left.add_leftmost(x)

    def add_rightmost(self, x):
        '''Find the rightmost node, add x to it.'''
        self.right.add_rightmost(x)

    def reduce_explode(self, depth=0):
        '''Reduce through exploding. Return something that evaluates to True or
        False, indicating success (or not). Use the return value to communicate
        what should replace, move left, and move right.'''
        if self.should_explode(depth):
            return self.explode()

        if self.left:
            result = self.left.reduce_explode(depth + 1)
            if result:
                if result[0] == 'explode':
                    d = result[1]
                    if 'replacement' in d:
                        self.left = d['replacement']
                        del d['replacement']
                    if 'right' in d:
                        self.right.add_leftmost(d['right'])
                        del d['right']

                    if d:
                        # there's still more to process up the chain
                        return 'explode', d

                return 'done', True

        if self.right:
            result = self.right.reduce_explode(depth + 1)
            if result:
                if result[0] == 'explode':
                    d = result[1]
                    if 'replacement' in d:
                        self.right = d['replacement']
                        del d['replacement']
                    if 'left' in d:
                        self.left.add_rightmost(d['left'])
                        del d['left']

                    if d:
                        # there's still more to process up the chain
                        return 'explode', d

                return 'done', True

        return False

    def reduce_split(self):
        '''Reduce through splitting. Return something that evaluates to True or
        False, indicating success (or not).'''

        if self.should_split():
            return self.split()

        if self.left:
            result = self.left.reduce_split()
            if result:
                if result[0] == 'split':
                    self.left = result[1]
                return 'done', True

        if self.right:
            result = self.right.reduce_split()
            if result:
                if result[0] == 'split':
                    self.right = result[1]
                return 'done', True

        return False

    def reduce(self):
        '''Reduce by exploding first, then splitting (in that priority
        order). My major mistake in my first implementation was taking the
        priority as the leftmost action available, and not prioritizing explodes
        over splits.'''
        r = self.reduce_explode()
        if r:
            return r
        return self.reduce_split()

class TreeLeaf(Tree):
    '''Special sub-class to represent leaf node values.'''
    def __init__(self, val):
        self.left = self.right = None
        self.val = val

    def copy(self): return TreeLeaf(self.val)
    def should_explode(self, depth): return False
    def add_leftmost(self, x): self.val += x
    def add_rightmost(self, x): self.val += x
    def should_split(self): return self.val >= 10

    def split(self):
        vDiv2 = self.val // 2
        r = Tree(TreeLeaf(vDiv2), TreeLeaf(self.val - vDiv2))
        return 'split', r

    def magnitude(self): return self.val
    def _str(self, depth): return str(self.val)
    def __repr__(self): return str(self.val)

def build_tree(x, depth=0):
    '''Build a tree from a nested list.'''
    if isinstance(x, int):
        return TreeLeaf(x)
    assert len(x) == 2
    assert depth <= 3
    left = build_tree(x[0], depth+1)
    right = build_tree(x[1], depth+1)
    return Tree(left, right)

def parse(line):
    '''Parse the nested list using the JSON library, then recursively build the
    tree.'''
    return build_tree(json.loads(line))

def part1(lines):
    '''Add all the numbers together (in order), continually reducing each
    result. Return the magnitude (a sort of checksum defined in the problem).'''
    t = parse(lines[0])
    for line in lines[1:]:
        t2 = parse(line)
        t = t.add(t2)
        while t.reduce():
            pass
    return t.magnitude()

def part2(lines):
    '''Try adding each pair of trees (in both orders: a+b, b+a), and reduce each
    result. Then find the magnitude. Return the maximum magnitude over all
    pairs.'''
    trees = list(map(parse, lines))
    max_magnitude = 0
    for i in range(len(trees)):
        for j in range(len(trees)):
            if i == j:
                continue

            # make copies, because the reduction process is destructive
            ti = trees[i].copy()
            tj = trees[j].copy()
            t = ti.add(tj)

            while t.reduce():
                pass

            max_magnitude = max(max_magnitude, t.magnitude())

    return max_magnitude

def main():
    regular_input = __file__.split('/')[-1][:-len('.py')] + '.in'
    file = regular_input if len(sys.argv) <= 1 else sys.argv[1]
    print(f'using input: {file}')
    with open(file) as f:
        lines = list(map(str.strip, f))

    print('part 1:', part1(lines))
    print('part 2:', part2(lines))

if __name__ == '__main__':
    main()

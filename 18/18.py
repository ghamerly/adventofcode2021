#!/usr/bin/env python3

# https://adventofcode.com/2021/day/18 - "snailfish"
# Author: Greg Hamerly

# One thing that could make this faster is caching the status of whether each
# node contains a descendant that should explode or split, and only descending
# into those branches where this is known to be true (or, avoiding descending
# branches where it's known to be false). But I've worked enough on this
# problem.

import sys
import json

class Tree:
    def __init__(self, left, right):
        self.children = [left, right]

    def copy(self):
        children = [c.copy() if c else None for c in self.children]
        return Tree(*children)

    def __repr__(self, depth=0):
        '''Display the tree in a way that highlights those pairs that should
        explode.'''
        a = '[' if depth < 4 else '('
        b = ']' if depth < 4 else ')'
        c0, c1 = self.children
        return f'{a}{c0.__repr__(depth+1)},{c1.__repr__(depth+1)}{b}'

    def magnitude(self):
        '''Find the "magnitude" -- a checksum defined by the problem -- for this
        tree.'''
        return 3 * self.children[0].magnitude() + 2 * self.children[1].magnitude()

    def explode(self):
        '''Explode the given pair, return a dictionary indicating what should
        replace, go left, and go right. Add 'done', which is never removed, so
        that the dictionary is never empty (and always evaluates to True).'''
        assert all(isinstance(c, TreeLeaf) for c in self.children)
        return {'replace': TreeLeaf(0),
                0: self.children[0].val,
                1: self.children[1].val,
                'done': True}

    def should_split(self):
        '''Trees that have children should never split.'''
        return False

    def should_explode(self, depth):
        '''Trees that are deep enough should explode.'''
        return depth >= 4

    def add_to_extreme_leaf(self, direction, value):
        '''Move as far as possible in "direction" (which is either 0 or 1), and
        add the given value to that leaf.'''
        self.children[direction].add_to_extreme_leaf(direction, value)

    def reduce_explode(self, depth=0):
        '''Reduce through exploding. Return something that evaluates to True or
        False, indicating success (or not). Use the return value to communicate
        what should replace, move left, and move right.'''
        if self.should_explode(depth):
            return self.explode()

        # look left, then right
        for node, sibling in [(0, 1), (1, 0)]:
            if self.children[node] is None:
                continue

            result = self.children[node].reduce_explode(depth + 1)
            if isinstance(result, dict):
                if 'replace' in result:
                    self.children[node] = result['replace']
                    del result['replace']
                if sibling in result:
                    self.children[sibling].add_to_extreme_leaf(node, result[sibling])
                    del result[sibling]

                return result

        return False

    def reduce_split(self):
        '''Reduce through splitting. Return something that evaluates to True or
        False, indicating success (or not).'''

        if self.should_split():
            return self.split()

        for node in range(2):
            if self.children[node]:
                result = self.children[node].reduce_split()
                if isinstance(result, dict):
                    if 'split' in result:
                        self.children[node] = result['split']
                        del result['split']
                    return result

        return False

    def _reduce(self):
        '''Reduce by exploding first, then splitting (in that priority
        order). My major mistake in my first implementation was taking the
        priority as the leftmost action available, and not prioritizing explodes
        over splits.'''
        r = self.reduce_explode()
        if r:
            return r
        return self.reduce_split()

    def reduce(self):
        '''Reduce until no further reduction can be done.'''
        while self._reduce():
            pass
        return self

class TreeLeaf(Tree):
    '''Special sub-class to represent leaf node values.'''
    def __init__(self, val):
        super().__init__(None, None)
        self.val = val

    def copy(self): return TreeLeaf(self.val)
    def should_explode(self, depth): return False
    def add_to_extreme_leaf(self, direction, value): self.val += value
    def should_split(self): return self.val >= 10

    def split(self):
        '''Split this leaf into a Tree with two leaves, according to the rules
        of the problem. Add 'done', which is never removed, so that the
        dictionary is never empty (and always evaluates to True).'''
        a = TreeLeaf(self.val // 2)
        b = TreeLeaf((self.val + 1) // 2)
        return {'split': Tree(a, b), 'done': True}

    def magnitude(self): return self.val
    def __repr__(self, depth=0):
        '''Highlight leaves whose values should be split.'''
        h = '*' if self.val >= 10 else ''
        return f'{h}{self.val}{h}'

def build(x, depth=0):
    '''Build a tree from a nested list.'''
    if isinstance(x, int):
        return TreeLeaf(x)
    assert len(x) == 2
    assert depth <= 3
    return Tree(build(x[0], depth+1), build(x[1], depth+1))

def parse(lines):
    '''Parse the nested list using the JSON library, then recursively build the
    tree.'''
    return [build(json.loads(l)) for l in lines]

def part1(lines):
    '''Add all the numbers together (in order), continually reducing each
    result. Return the magnitude (a sort of checksum defined in the problem).'''
    trees = parse(lines)
    t = trees[0]
    for t2 in trees[1:]:
        t = Tree(t, t2).reduce()
    return t.magnitude()

def part2(lines):
    '''Try adding each pair of trees (in both orders: a+b, b+a), and reduce each
    result. Then find the magnitude. Return the maximum magnitude over all
    pairs.'''
    trees = parse(lines)
    magnitudes = []
    for i, ti in enumerate(trees):
        for j, tj in enumerate(trees):
            if i != j:
                # make copies, because the reduction process is destructive
                magnitudes.append(Tree(ti.copy(), tj.copy()).reduce().magnitude())

    return max(magnitudes)

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

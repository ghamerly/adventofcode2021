#!/usr/bin/env python3

# https://adventofcode.com/2021/day/12 - "path counting"
# Author: Greg Hamerly

import sys
import collections

def dfs(graph, visit_count, current, two_small_allowed, path):
    '''Perform a DFS on the graph at the current node. Visit "small" (lowercase)
    nodes at most once (though for any path, twice is allowed for any one small
    node if two_small_allowed is True). If we are allowed to visit this node,
    add 1 to the visit_count of the visited node.'''

    # The "end" node is treated specially; we may always visit it, but never
    # pass through it.
    if current == 'end':
        visit_count[current] += 1
        return

    # visit small nodes at most once (or one small node twice if
    # two_small_allowed is True; set it False for deeper recursion).
    if visit_count[current] and 'a' <= current[0] <= 'z':
        if two_small_allowed:
            two_small_allowed = False
        else:
            return

    # update the visit_count, the path, and visit all neighbors
    visit_count[current] += 1
    path.append(current)
    for v in graph[current]:
        if v != 'start': # we cannot revisit the start, ever
            dfs(graph, visit_count, v, two_small_allowed, path)
    path.pop()
    visit_count[current] -= 1

def solve(graph, two_small_allowed):
    '''A generalization of part1 and part2.'''
    visit_count = {u: 0 for u in graph}
    dfs(graph, visit_count, 'start', two_small_allowed, [])
    return visit_count['end']

def part1(graph):
    '''Count the unique paths that never revisit any small node.'''
    return solve(graph, False)

def part2(graph):
    '''Count the unique paths that revisit one small node at most once per
    path.'''
    return solve(graph, True)

def parse(lines):
    graph = collections.defaultdict(set)
    for line in lines:
        u, v = line.split('-')
        graph[u].add(v)
        graph[v].add(u)
    return graph

def main():
    regular_input = __file__.split('/')[-1][:-len('.py')] + '.in'
    file = regular_input if len(sys.argv) <= 1 else sys.argv[1]
    print(f'using input: {file}')
    with open(file) as f:
        lines = list(map(str.strip, f))

    graph = parse(lines)

    print('part 1:', part1(graph))
    print('part 2:', part2(graph))

if __name__ == '__main__':
    main()

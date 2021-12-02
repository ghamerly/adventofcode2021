#!/usr/bin/env python3

def part1(cmds):
    x = y = 0
    for c, d in cmds:
        if c == 'forward':
            x += d
        elif c == 'down':
            y += d
        elif c == 'up':
            y -= d

    return x * y

def part2(cmds):
    aim = x = y = 0
    for c, d in cmds:
        if c == 'forward':
            y += aim * d
            x += d
        elif c == 'down':
            aim += d
        elif c == 'up':
            aim -= d

    return x * y


def main():
    with open('2.in') as f:
        cmds = [(a, int(b)) for a, b in map(str.split, f)]

    print('part 1:', part1(cmds))
    print('part 2:', part2(cmds))

if __name__ == '__main__':
    main()

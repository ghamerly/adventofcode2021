#!/usr/bin/env python3

def part1(v):
    increases = 0
    for i in range(1, len(v)):
        if v[i-1] < v[i]:
            increases += 1
    return increases

def part2(v):
    increases = 0
    s = v[0] + v[1] + v[2]
    for i in range(3, len(v)):
        s2 = s - v[i - 3] + v[i]
        if s < s2:
            increases += 1
        s = s2
    return increases

def main():
    with open('1.in') as f:
        v = list(map(int, f))

    print('part 1:', part1(v))
    print('part 2:', part2(v))

if __name__ == '__main__':
    main()

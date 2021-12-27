#!/usr/bin/env python3

# https://adventofcode.com/2021/day/24 - "arithmetic logic unit"
# Author: Greg Hamerly

# The approach here is to build the expression that computes the last value of
# "z", as a tree. Re-use nodes rather than deep copy them. Treat each input as a
# variable that can produce values 1-9. Simplify expressions whenever it is
# provably possible to do so.
#
# Then search for the values that can cause the expression for "z" to produce 0.
# Start by assuming each variable can produce all values. Progressively limit
# the values and see if they can still produce 0. Search largest-to-smallest
# (for part 1) and smallest-to-largest (part 2).
#
# Part 1 runs quickly (about a minute), because the answer is very large.
# Part 2 is slow, requiring hours.
#
# Ways to speed this up:
#   - use smarter caching (don't blow away the cache of values every time)
#   - instead of generating all possible values, just check that 0 is able to
#     be produced

import sys
import time

class BaseExpression:
    def __init__(self):
        super().__init__()
        self.cached_possible_values = set()

    def reset_possible_cache(self):
        self.cached_possible_values = set()

    def possible_values(self):
        if not self.cached_possible_values:
            self.cached_possible_values = set(self._possible_values())
        return self.cached_possible_values

    def simplify(self):
        return self

    def size(self):
        return 1

class Constant(BaseExpression):
    def __init__(self, value):
        super().__init__()
        self.value = int(value)

    def __add__(self, other):
        return Constant(self.value + other.value)

    def __mod__(self, other):
        return Constant(self.value % other.value)

    def __floordiv__(self, other):
        # round towards zero, even for negative numbers
        return Constant(int(self.value / other.value))

    def __mul__(self, other):
        return Constant(self.value * other.value)

    def __eq__(self, other):
        o = other.value if isinstance(other, Constant) else other
        return True if self.value == o else False

    def __repr__(self):
        return str(self.value)

    def _possible_values(self):
        yield self.value

class BinaryOp(BaseExpression):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right

    def __repr__(self):
        return f'({self.left} {self.opname()} {self.right})'

    def reset_possible_cache(self):
        super().reset_possible_cache()
        self.left.reset_possible_cache()
        self.right.reset_possible_cache()

    def simplify(self):
        for i, v in enumerate(self.possible_values()):
            if i == 1:
                return self
        print(f'Replacing {self} with {v}')
        return Constant(v)

    def _possible_values(self):
        left_values = list(self.left.possible_values())
        right_values = list(self.right.possible_values())
        seen = set()

        for l in left_values:
            for r in right_values:
                try:
                    v = self.op(l, r)
                    if v not in seen:
                        seen.add(v)
                        yield v
                except ZeroDivisionError:
                    pass

    def op(self, left, right):
        assert False

    def size(self):
        return self.left.size() + self.right.size() + 1

class AddOp(BinaryOp):
    def __init__(self, left, right): super().__init__(left, right)
    def op(self, left, right): return left + right
    def opname(self): return '+'
    def simplify(self):
        if self.left == self.right:
            print('ADDOP SIMPLIFY SHORTCUT')
            return MulOp(self.left, Constant(2))
        return super().simplify()

class MulOp(BinaryOp):
    def __init__(self, left, right): super().__init__(left, right)
    def op(self, left, right): return left * right
    def opname(self): return '*'

class DivOp(BinaryOp):
    def __init__(self, left, right): super().__init__(left, right)
    # round towards zero, even for negative numbers
    def op(self, left, right): return int(left / right)
    def opname(self): return '/'

class ModOp(BinaryOp):
    def __init__(self, left, right): super().__init__(left, right)
    def op(self, left, right): return left % right
    def opname(self): return '%'

class EqlOp(BinaryOp):
    def __init__(self, left, right): super().__init__(left, right)
    def op(self, left, right): return 1 if left == right else 0
    def opname(self): return '='

    def simplify(self):
        if self.left == self.right:
            print('EQUAL SIMPLIFY SHORTCUT')
            return Constant(1)
        return super().simplify()

class Variable(BaseExpression):
    def __init__(self, var_id, *rules):
        super().__init__()
        self.var_id = var_id
        self.rules = rules[:]
        self.values = list(range(1, 10))

    def set_values(self, values):
        self.values = values

    def __repr__(self):
        return f'input{self.var_id}'

    def _possible_values(self):
        return self.values

class Rule:
    def __init__(self):
        pass

class RangeRule(Rule):
    def __init__(self, rng):
        self.range = rng

    def __call__(self, other):
        return other in self.range

def get_b_const(state, b):
    if isinstance(b, Constant):
        return b, True
    return state[b], isinstance(state[b], Constant)

def add(state, a, b):
    b, b_is_const = get_b_const(state, b)

    a_is_const = isinstance(state[a], Constant)

    if b_is_const:
        if b == 0:
            return

        if a_is_const:
            state[a] = state[a] + b
        else:
            state[a] = AddOp(state[a], b)
    elif a_is_const and state[a] == 0:
        state[a] = b
    else:
        state[a] = AddOp(state[a], b)

def div(state, a, b):
    b, b_is_const = get_b_const(state, b)

    a_is_const = isinstance(state[a], Constant)

    if b_is_const:
        if b == 1:
            return

        if a_is_const:
            state[a] = state[a] // b
        else:
            state[a] = DivOp(state[a], b)
    elif a_is_const and state[a] == 0:
        return
    else:
        state[a] = DivOp(state[a], b)

def eql(state, a, b):
    b, b_is_const = get_b_const(state, b)

    a_is_const = isinstance(state[a], Constant)

    if a_is_const and b_is_const:
        state[a] = Constant(1 if state[a] == b else 0)
    elif a_is_const or b_is_const:
        x, y = (state[a], b) if a_is_const else (b, state[a])
        if x.value in y.possible_values():
            state[a] = EqlOp(state[a], b)
        else:
            state[a] = Constant(0)
    elif set(state[a].possible_values()) & set(b.possible_values()):
        state[a] = EqlOp(state[a], b)
    else:
        state[a] = Constant(0)

VARIABLES = []

def inp(state, a):
    var_id = len(VARIABLES)
    v = Variable(var_id, RangeRule(list(range(1, 10))))
    VARIABLES.append(v)
    state[a] = v

def mod(state, a, b):
    b, b_is_const = get_b_const(state, b)

    a_is_const = isinstance(state[a], Constant)

    if b_is_const:
        if a_is_const:
            state[a] = state[a] % b
        else:
            state[a] = ModOp(state[a], b)
    elif a_is_const and (state[a] == 0 or state[a] == 1):
        return
    else:
        state[a] = ModOp(state[a], b)

def mul(state, a, b):
    b, b_is_const = get_b_const(state, b)

    a_is_const = isinstance(state[a], Constant)

    if b_is_const:
        if b == 1:
            return
        if b == 0:
            state[a] = Constant(0)
            return
        if a_is_const:
            state[a] = state[a] * b
        else:
            state[a] = MulOp(state[a], b)
    elif a_is_const and (state[a] == 0 or state[a] == 1):
        if state[a] == Constant(0):
            return
        state[a] = b
    else:
        state[a] = MulOp(state[a], b)

COUNT = 0

SEARCH_ORDER_PART1 = [9, 8, 7, 6, 5, 4, 3, 2, 1]
SEARCH_ORDER_PART2 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
SEARCH_ORDER = None

def search(expression, var_ndx):
    global COUNT, SEARCH_ORDER
    print('search', var_ndx)
    if var_ndx == len(VARIABLES):
        return True

    COUNT += 1
    if COUNT % 50 == 0:
        v = []
        for var in VARIABLES:
            if len(var.values) == 1:
                v.append(var.values[0])
            else:
                v.append('?')
        print(COUNT, ''.join(map(str, v)))

    for v in SEARCH_ORDER:
        VARIABLES[var_ndx].set_values([v])
        expression.reset_possible_cache()
        vals = expression.possible_values()
        assert vals
        if 0 in vals:
            if search(expression, var_ndx + 1):
                return True

    VARIABLES[var_ndx].set_values(list(range(1, 10)))

def parse_alu(lines):
    state = {'w': Constant(0), 'x': Constant(0), 'y': Constant(0), 'z': Constant(0)}

    ops = { name: globals()[name] for name in ['add', 'div', 'eql', 'inp', 'mod', 'mul'] }

    for i, line in enumerate(lines):
        tokens = line.split()

        cmd = tokens[0]

        args = []
        for t in tokens[1:]:
            if t in 'wxyz':
                args.append(t)
            else:
                args.append(Constant(t))

        print(f'{i}/{len(lines)}: {cmd}{tuple(args)}')
        ops[cmd](state, *args)
       # uncomment if using simplification
       #t1 = time.process_time()
       #state[args[0]] = state[args[0]].simplify()
       #t2 = time.process_time()
       #print(f'size of {args[0]}: {state[args[0]].size()}')
       #t3 = time.process_time()
       #t_delta = t2 - t1
       #if t_delta > 1:
       #    print(f'time to simplify: {t_delta:0.2f}')

    return state['z']

def reset_variables():
    global VARIABLES
    for v in VARIABLES:
        v.set_values(list(range(1, 10)))

def part1(expression):
    global SEARCH_ORDER
    SEARCH_ORDER = SEARCH_ORDER_PART1

    reset_variables()

    ans = 0
    if search(expression, 0):
        for v in VARIABLES:
            ans = ans * 10 + v.values[0]
    else:
        print('NO SOLUTION')

    return ans

def part2(expression):
    global SEARCH_ORDER
    SEARCH_ORDER = SEARCH_ORDER_PART2

    reset_variables()

    ans = 0
    if search(expression, 0):
        for v in VARIABLES:
            ans = ans * 10 + v.values[0]
    else:
        print('NO SOLUTION')

    return ans

def main():
    regular_input = __file__.split('/')[-1][:-len('.py')] + '.in'
    file = regular_input if len(sys.argv) <= 1 else sys.argv[1]
    print(f'using input: {file}')
    with open(file) as f:
        lines = list(map(str.strip, f))

    expression = parse_alu(lines)

    print('part 1:', part1(expression))
    print('part 2:', part2(expression))

if __name__ == '__main__':
    main()

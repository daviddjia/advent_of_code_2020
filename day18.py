#!/bin/env/python

f = open('day18_input.txt', 'r')
lines = [line.strip() for line in f.readlines()]

def eval_op(expr1, expr2, op, part):
    if op == '+':
        if part == 2 and isinstance(expr1[-1], int) and isinstance(expr2[0], int):
            return solve(expr1[0:-1] + [expr1[-1]+expr2[0]] + expr2[1:], part=part)
        elif part == 2:
            if isinstance(expr1[-1], int):
                val1_start_index = len(expr1)-1
                addend1 = expr1[-1]
            else:
                close_count = 0
                for j, char in enumerate(reversed(expr1)):
                    if char == ')':
                        close_count += 1
                    elif char == '(' and close_count > 1:
                        close_count -= 1
                    elif char == '(':
                        val1_start_index = len(expr1)-1-j
                        addend1 = solve(expr1[val1_start_index:], part=part)
                        break
            if isinstance(expr2[0], int):
                val2_end_index = 1
                addend2 = expr2[0]
            else:
                open_count = 0
                for j, char in enumerate(expr2):
                    if char == '(':
                        open_count += 1
                    elif char == ')' and open_count > 1:
                        open_count -= 1
                    elif char == ')':
                        val2_end_index = j+1
                        addend2 = solve(expr2[:val2_end_index], part=part)
                        break
            return solve(
                expr1[:val1_start_index] + [solve(
                    addend1+addend2,
                    part=part)] + expr2[val2_end_index:],
                part=part,
            )
        else:
            return solve(expr1, part=part) + solve(expr2, part=part)
    else:
        return solve(expr1, part=part) * solve(expr2, part=part)

def solve(expr, part):
    if isinstance(expr, int):
        return expr
    elif len(expr) == 1:
        return expr[0]
    elif len(expr) == 3:
        return eval_op([expr[0]], [expr[2]], expr[1], part=part)
    elif isinstance(expr[0], int):
        return eval_op([expr[0]], expr[2:], expr[1], part=part)
    elif expr[0] == '(':
        open_count = 0
        for i, char in enumerate(expr):
            if char == '(':
                open_count += 1
            elif char == ')' and open_count > 1:
                open_count -= 1
            elif char == ')':
                if i < len(expr)-1:
                    return eval_op([solve(expr[1:i], part=part)], expr[i+2:], expr[i+1], part=part)
                else:
                    return solve(expr[1:i], part=part)

def solve_all(lines, part):
    result_sum = 0
    for line in lines:
        expr = []
        for char in reversed(line):
            if char == ' ':
                continue
            elif char == '(':
                expr.append(')')
            elif char == ')':
                expr.append('(')
            elif char in ('+', '*'):
                expr.append(char)
            else:
                expr.append(int(char))
        result_sum += solve(expr, part=part)
    return result_sum

print(solve_all(lines, part=1))
print(solve_all(lines, part=2))

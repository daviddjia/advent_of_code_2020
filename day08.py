#!/bin/env/python

f = open('day08_input.txt', 'r')
lines = [line.strip() for line in f.readlines()]

run_lines = set()
acc = 0
pointer = 0
while pointer not in run_lines:
    line = lines[pointer]
    instruction, param = line.split()
    param = int(param)

    run_lines.add(pointer)

    if instruction == 'acc':
        acc += param
        pointer += 1
    elif instruction == 'jmp':
        pointer += param
    else:
        pointer += 1
print(acc)

for change_from, change_to in [('jmp', 'nop'), ('nop', 'jmp')]:
    error_lines = [
        i
        for i, line in enumerate(lines)
        if line.split()[0] == change_from]

    for error_line_pointer in error_lines:
        error_line = lines[error_line_pointer]

        run_lines = set()
        acc = 0
        pointer = 0
        while pointer not in run_lines and pointer != len(lines):
            line = lines[pointer]
            instruction, param = line.split()
            param = int(param)
            if pointer == error_line_pointer:
                instruction = change_to

            run_lines.add(pointer)

            if instruction == 'acc':
                acc += param
                pointer += 1
            elif instruction == 'jmp':
                pointer += param
            else:
                pointer += 1

        if pointer == len(lines):
            print(acc)
            break

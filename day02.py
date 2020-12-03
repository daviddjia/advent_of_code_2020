#!/bin/env/python

f = open('day02_input.txt', 'r')

lines = f.readlines()

total_valid = 0
for l in lines:
    [count_range, char, pw] = l.split(' ')
    count_range = [int(cr) for cr in count_range.split('-')]
    char = char[:-1]

    letter_count = 0
    for p in pw:
        if p == char:
            letter_count += 1
    if letter_count >= count_range[0] and letter_count <= count_range[1]:
        total_valid += 1

print(total_valid)

total_valid = 0
for l in lines:
    [indexes, char, pw] = l.split(' ')
    indexes = [int(i) for i in indexes.split('-')]
    char = char[:-1]

    if (pw[indexes[0]-1] == char) != (pw[indexes[1]-1] == char):
        total_valid += 1

print(total_valid)

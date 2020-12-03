#!/bin/env/python

f = open('day03_input.txt', 'r')

lines = [l.strip() for l in f.readlines()]

count = 0
j = 0
for i, line in enumerate(lines):
    if line[j] == '#':
        count += 1
    j = (j+3)%(len(line))
print(count)

slopes = [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]
counts = []
for slope in slopes:
    count = 0
    i = 0
    j = 0
    while i < len(lines):
        if lines[i][j] == '#':
            count += 1
        i += slope[0]
        j = (j+slope[1])%(len(lines[0]))
    counts.append(count)
product = 1
for c in counts:
    product *= c
print(product)

#!/bin/env/python

f = open('day06_input.txt', 'r')

lines = [line.strip() for line in f.readlines()]

groups = []
group = ''
for line in lines:
    if line == '':
        groups.append(group.strip())
        group = ''
    else:
        group += line
groups.append(group.strip())

count = 0
for group in groups:
    count += len(list(set(list(group))))
print(count)

groups = []
group = []
for line in lines:
    if line == '':
        groups.append(group)
        group = []
    else:
        group.append(line)
groups.append(group)

count = 0
for group in groups:
    intersection = set()
    for i, person in enumerate(group):
        person_set = set(list(person))
        if i == 0:
            intersection = person_set
        else:
            intersection = intersection.intersection(person_set)
    count += len(list(intersection))
print(count)

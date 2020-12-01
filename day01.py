#!/bin/env/python

f = open('day01_input.txt', 'r')

lines = [int(i) for i in f.readlines()]

for i in range(0, len(lines)):
    for j in range(i+1, len(lines)):
        if lines[i]+lines[j] == 2020:
            print(lines[i]*lines[j])

for i in range(0, len(lines)):
    for j in range(i+1, len(lines)):
        for k in range(j+1, len(lines)):
            if lines[i]+lines[j]+lines[k] == 2020:
                print(lines[i]*lines[j]*lines[k])

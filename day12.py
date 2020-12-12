#!/bin/env/python

f = open('day12_input.txt', 'r')

directions = [line.strip() for line in f.readlines()]

x, y, facing = 0, 0, 0
for direction in directions:
    action = direction[0]
    value = int(direction[1:])
    if action == 'F':
        if facing == 0:
            action = 'E'
        elif facing == 90:
            action = 'N'
        elif facing == 180:
            action = 'W'
        elif facing == 270:
            action = 'S'
    if action == 'N':
        y += value
    elif action == 'S':
        y -= value
    elif action == 'E':
        x += value
    elif action == 'W':
        x -= value
    elif action == 'L':
        facing = (facing + value) % 360
    elif action == 'R':
        facing = (facing - value) % 360
print(abs(x)+abs(y))

x, y, i, j = 0, 0, 10, 1
rotate_map = { # counter clockwise
    90: lambda i,j: (-j, i),
    180: lambda i,j: (-i, -j),
    270: lambda i,j: (j, -i),
}
for direction in directions:
    action = direction[0]
    value = int(direction[1:])

    if action == 'F':
        x += i*value
        y += j*value
    elif action == 'N':
        j += value
    elif action == 'S':
        j -= value
    elif action == 'E':
        i += value
    elif action == 'W':
        i -= value
    elif action == 'L':
        (i, j) = rotate_map[value](i, j)
    elif action == 'R':
        (i, j) = rotate_map[(-value)%360](i, j)
print(abs(x)+abs(y))

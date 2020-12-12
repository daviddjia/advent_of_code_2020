#!/bin/env/python

from copy import deepcopy

f = open('day11_input.txt', 'r')

seats = [[state for state in line.strip()] for line in f.readlines()]

def get_num_occupied(seats, i, j, social_distance):
    moves = [
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1)]
    count = 0
    for move in moves:
        x, y = i + move[0], j + move[1]
        if social_distance:
            while 0 <= x < len(seats) and 0 <= y < len(seats[0]) and seats[x][y] == '.':
                x, y = x + move[0], y + move[1]
        if 0 <= x < len(seats) and 0 <= y < len(seats[0]) and seats[x][y] == '#':
            count += 1
    return count

def seat_simulation(seats, social_distance, people_limit):
    seat_changed = True
    while seat_changed:
        state_changes = []
        for i, row in enumerate(seats):
            for j, state in enumerate(row):
                if state == '.':
                    continue
                num_occupied = get_num_occupied(seats, i, j, social_distance)
                if (
                    (state == 'L' and num_occupied == 0)
                    or (state == '#' and num_occupied >= people_limit)
                ):
                    state_changes.append((i,j))
        seat_changed = bool(state_changes)
        for (i, j) in state_changes:
            seats[i][j] = '#' if seats[i][j] == 'L' else 'L'

    occupied_count = 0
    for i, row in enumerate(seats):
        for j, state in enumerate(row):
            if seats[i][j] == '#':
                occupied_count += 1
    return occupied_count

print(seat_simulation(deepcopy(seats), social_distance=False, people_limit=4))
print(seat_simulation(deepcopy(seats), social_distance=True, people_limit=5))

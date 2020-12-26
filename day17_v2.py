#!/bin/env/python

from itertools import product
from functools import reduce

f = open('day17_input.txt', 'r')
initial_grid = [list(line.strip()) for line in f.readlines()]

def possible_adjacent_diff(coord, dim):
    x, y, z, w = coord
    adj_diffs = set(product({-1, 0, 1},repeat = dim))
    if dim == 3:
        adj_diffs.remove((0, 0, 0))
    else:
        adj_diffs.remove((0, 0, 0, 0))
    return [
        

def num_active_adjacents(grid, coord, dim):
    x, y, z, w = coord
    num_active = 0
    for adj_diff in adj_diffs:
        (i, j, k), l = adj_diff[0:3], 0 if dim == 3 else adj_diff[3]
        if grid[w+l][z+k][x+i][y+j] == '#':
                num_active += 1
    return num_active

def simulate_cubes(initial_grid, dim):
    # Initialize grid
    grid = {
        (x, y, 0, 0):
        for x, row in enumerate(initial_grid)
        for y, cube in enumerate(row)
    }

    # Simulate 6 rounds
    for t in range(6):
        coords_to_change = []
        for w, space in enumerate(grid):
            for z, plane in enumerate(space):
                for x, row in enumerate(plane):
                    for y, cube in enumerate(row):
                        num_active_adj = num_active_adjacents(
                            grid,
                            (x, y, z, w),
                            dim)
                        if cube == '#' and num_active_adj not in [2, 3]:
                            coords_to_change.append((x, y, z, w))
                        elif cube == '.' and num_active_adj == 3:
                            coords_to_change.append((x, y, z, w))
        for x, y, z, w in coords_to_change:
            grid[w][z][x][y] = '#' if grid[w][z][x][y] == '.' else '.'

    # Count actives
    active_count = 0
    for w, space in enumerate(grid):
        for z, plane in enumerate(space):
            for x, row in enumerate(plane):
                for y, cube in enumerate(row):
                    if cube == '#':
                        active_count += 1
    return active_count

print(simulate_cubes(initial_grid, 3))
print(simulate_cubes(initial_grid, 4))

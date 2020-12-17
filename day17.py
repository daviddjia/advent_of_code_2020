#!/bin/env/python

from itertools import product
from functools import reduce

f = open('day17_input.txt', 'r')
initial_grid = [list(line.strip()) for line in f.readlines()]

def num_active_adjacents(grid, coord, dim):
    x, y, z, w = coord
    adj_diffs = set(product({-1, 0, 1},repeat = dim))
    adj_diffs.remove((0, 0, 0) if dim == 3 else (0, 0, 0, 0))
    num_active = 0
    for adj_diff in adj_diffs:
        (i, j, k), l = adj_diff[0:3], 0 if dim == 3 else adj_diff[3]
        if (
            0 <= w+l < len(grid)
            and 0 <= z+k < len(grid[0])
            and 0 <= x+i < len(grid[0][0])
            and 0 <= y+j < len(grid[0][0][0])
        ):
            if grid[w+l][z+k][x+i][y+j] == '#':
                num_active += 1
    return num_active

def simulate_cubes(initial_grid, dim):
    # Initialize grid
    grid = [[[
        ['.' for _ in range(len(initial_grid[0])+12)]
        for _ in range(len(initial_grid)+12)
    ] for _ in range(13)] for _ in range(1 if dim == 3 else 13)]
    for i, row in enumerate(initial_grid):
        for j, cube in enumerate(row):
            grid[0 if dim == 3 else 6][6][i+6][j+6] = cube

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

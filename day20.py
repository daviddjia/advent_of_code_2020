#!/bin/env/python

from functools import reduce
from copy import deepcopy

class Tile(object):
    def _calculate_borders(self):
        old_borders = {} if not self.borders else {
            k: v for k, v in
            self.borders.items()
        }

        self.borders['top'] = self.grid[0]
        self.borders['bottom'] = self.grid[-1][::-1]
        self.borders['left'] = (''.join([row[0] for row in self.grid]))[::-1]
        self.borders['right'] = ''.join([row[-1] for row in self.grid])

        if old_borders:
            orientation_map = {}
            for old_orientation, old_border in old_borders.items():
                orientation_map[old_orientation] = [
                    orientation for orientation, border in self.borders.items()
                    if old_border == border or old_border == border[::-1]
                ][0]
            new_adjacents = {}
            for orientation, (adj_tile, adj_orientation) in self.adjacents.items():
                new_orientation = orientation_map[orientation]
                new_adjacents[new_orientation] = self.adjacents[orientation]
                adj_tile.adjacents[adj_orientation] = (self, new_orientation)
            self.adjacents = new_adjacents

    def __init__(self, num, grid):
        self.num = num
        self.grid = grid

        self.borders = {}
        self._calculate_borders()

        self.adjacents = {}

    angle_map = {
        'right': 3,
        'bottom': 2,
        'left': 1,
        'top': 0,
    }

    def clockwise_rotate(self, angle):
        for _ in range(angle//90):
            self.grid = list(list(x)[::-1] for x in zip(*self.grid))
        self.grid = [''.join(row) for row in self.grid]
        self._calculate_borders()

    def flip(self, direction):
        height = len(self.grid)
        if direction == 'h':
            for i in range(height):
                self.grid[i] = self.grid[i][::-1]
        else:
            for i in range(height//2):
                self.grid[i], self.grid[height-1-i] = self.grid[height-1-i], self.grid[i]
        self._calculate_borders()

    def reorient_starting_corner(self):
        orientations = tuple(self.adjacents.keys())
        angle_diff = self.angle_map[orientations[0]] - self.angle_map[orientations[1]]
        if angle_diff % 4 == 1:
            rotate_num = (self.angle_map[orientations[0]] - self.angle_map['right']) % 4
        else:
            rotate_num = (self.angle_map[orientations[1]] - self.angle_map['right']) % 4
        self.clockwise_rotate(rotate_num*90)

    def reorient(self, adj_tile, adj_orientation):
        orientation = [
            o for o, (t, _) in self.adjacents.items()
            if t.num == adj_tile.num
        ][0]
        angle_diff = 2 + self.angle_map[orientation] - self.angle_map[adj_orientation]
        self.clockwise_rotate(angle_diff % 4 * 90)

        orientation = [
            o for o, (t, _) in self.adjacents.items()
            if t.num == adj_tile.num
        ][0]
        if self.borders[orientation] == adj_tile.borders[adj_orientation]:
            if orientation in ('top', 'bottom'):
                self.flip('h')
            elif orientation in ('left', 'right'):
                self.flip('v')

    @property
    def real_grid(self):
        return [row[1:-1] for row in self.grid[1:-1]]

    def __repr__(self):
        return str(self.num)

    def __str__(self):
        return str(self.num)

class MonsterBuilder(object):
    def __init__(self, pattern):
        self.monster = [list(line) for line in pattern]

    def _get_rotations(self, monster):
        rotations = []
        rotated_monster = monster
        for _ in range(3):
            rotated_monster = list(list(x)[::-1] for x in zip(*rotated_monster))
            rotations.append(rotated_monster)
        return rotations

    def _get_flips(self, monster):
        flipped_monster = deepcopy(monster)
        height = len(monster)
        for i in range(height//2):
            flipped_monster[i], flipped_monster[height-1-i] = flipped_monster[height-1-i], flipped_monster[i]
        return flipped_monster

    @property
    def all_orientations(self):
        all_orientations = [self.monster]
        all_orientations.append(self._get_flips(self.monster))
        rotations = []
        for monster in all_orientations:
            rotations.extend(self._get_rotations(monster))
        all_orientations.extend(rotations)
        return all_orientations

def parse_input():
    f = open('day20_input.txt', 'r')
    lines = [line.strip() for line in f.readlines()]

    tiles = {}
    tile_num = -1
    grid = []
    for line in lines:
        if 'Tile' in line:
            tile_num = int(line.split(' ')[1][:-1])
        elif not line:
            tiles[tile_num] = Tile(tile_num, grid)
            grid = []
        else:
            grid.append(line)
    return tiles

def find_adjacents(tiles):
    unmatched_borders = {}
    for tile in tiles.values():
        for orientation, border in tile.borders.items():
            if (
                orientation not in tile.adjacents
                and (border in unmatched_borders
                or border[::-1] in unmatched_borders)
            ):
                adj_border = border if border in unmatched_borders else border[::-1]
                adj_tile, adj_orientation = unmatched_borders[adj_border]
                tile.adjacents[orientation] = (adj_tile, adj_orientation)
                adj_tile.adjacents[adj_orientation] = (tile, orientation)
                del unmatched_borders[adj_border]
            else:
                unmatched_borders[border] = (tile, orientation)
    return unmatched_borders

def get_corner_nums(unmatched_borders):
    tile_count = {}
    for border, (tile, orientation) in unmatched_borders.items():
        if tile.num in tile_count:
            tile_count[tile.num] += 1
        else:
            tile_count[tile.num] = 1
    return [tile for tile, count in tile_count.items() if count==2]

def plot_image(tiles, corner):
    image_grid = [[corner]]
    corner.reorient_starting_corner()

    tile, orientation = corner, 'bottom'
    while orientation in tile.adjacents:
        adj_tile, _ = tile.adjacents[orientation]
        image_grid.append([adj_tile])
        adj_tile.reorient(tile, orientation)
        tile = adj_tile

    for image_row in image_grid:
        tile, orientation = image_row[0], 'right'
        while orientation in tile.adjacents:
            adj_tile, _ = tile.adjacents[orientation]
            image_row.append(adj_tile)
            adj_tile.reorient(tile, orientation)
            tile = adj_tile
    return image_grid

def build_image(image_grid):
    tile_height = len(image_grid[0][0].real_grid)
    image = [[] for _ in range(len(image_grid)*tile_height)]
    for i, row in enumerate(image_grid):
        for tile in row:
            tile_grid = tile.real_grid
            for j, tile_row in enumerate(tile_grid):
                image[tile_height*i+j].extend(list(tile_row))
    return image

def identify_monsters(image_grid):
    monster_builder = MonsterBuilder([
        '                  # ',
        '#    ##    ##    ###',
        ' #  #  #  #  #  #   ',
    ])
    for monster in monster_builder.all_orientations:
        for i, row in enumerate(image[:-(len(monster)-1)]):
            for j, pos in enumerate(row[:-(len(monster[0])-1)]):
                found = True
                for k, mrow in enumerate(monster):
                    for l, mpos in enumerate(mrow):
                        if mpos == '#' and mpos != image[i+k][j+l]:
                            found = False
                            break
                    if found == False:
                        break
                if found:
                    for k, mrow in enumerate(monster):
                        for l, mpos in enumerate(mrow):
                            if mpos == '#':
                                image[i+k][j+l] = 'O'

def calculate_water_density(image):
    count = 0
    for i, row in enumerate(image):
        for j, pos in enumerate(row):
            if pos == '#':
                count += 1
    return count

tiles = parse_input()
corner_nums = get_corner_nums(find_adjacents(tiles))
print(reduce(lambda x,y:x*y, corner_nums))

image = build_image(plot_image(tiles, tiles[corner_nums[0]]))
identify_monsters(image)
# for row in image:
    # print(''.join(row))
print(calculate_water_density(image))

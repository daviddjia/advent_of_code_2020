#!/bin/env/python

class Hexagon(object):
    def __init__(self, coord):
        self.coord = coord
        self.color = 0 # white

    def flip(self):
        self.color = 0 if self.color else 1
        return self.color

class HexTile(object):
    move_coords = {
        'e': (1, 0),
        'w': (-1, 0),
        'ne': (1, 1),
        'nw': (0, 1),
        'se': (0, -1),
        'sw': (-1, -1),
    }

    def __init__(self):
        self.ref_tile = Hexagon((0, 0))
        self.black_count = 0
        self.tiles = {(0, 0): self.ref_tile}

    def add_coords(self, coord1, coord2):
        return tuple(map(sum, zip(
            coord1,
            coord2,
        )))

    def flip_tile(self, direction):
        tile = self.ref_tile
        for move in direction:
            new_coord = self.add_coords(tile.coord, self.move_coords[move])
            if new_coord not in self.tiles:
                tile = Hexagon(new_coord)
                self.tiles[new_coord] = tile
            else:
                tile = self.tiles[new_coord]

        if tile.flip():
            self.black_count += 1
        else:
            self.black_count -= 1

    def surround_black_tiles(self):
        coords_to_add = set()
        for coord, tile in self.tiles.items():
            if tile.color:
                for move_coord in self.move_coords.values():
                    adj_coord = self.add_coords(tile.coord, move_coord)
                    if adj_coord not in self.tiles:
                        coords_to_add.add(adj_coord)
        for coord in coords_to_add:
            tile = Hexagon(coord)
            self.tiles[coord] = tile

    def artistic_flip(self):
        tiles_to_flip = []
        for coord, tile in self.tiles.items():
            adj_black_count = 0
            for move_coord in self.move_coords.values():
                adj_coord = self.add_coords(tile.coord, move_coord)
                if adj_coord in self.tiles:
                    color = self.tiles[adj_coord].color
                    if color:
                        adj_black_count += 1

            if tile.color and (adj_black_count == 0 or adj_black_count > 2):
                tiles_to_flip.append(tile)
            elif not tile.color and adj_black_count == 2:
                tiles_to_flip.append(tile)

        for tile in tiles_to_flip:
            if tile.flip():
                self.black_count += 1
            else:
                self.black_count -= 1

def parse_input():
    f = open('day24_input.txt', 'r')
    lines = [line.strip() for line in f.readlines()]
    directions = []
    for line in lines:
        direction, move = [], ''
        for char in line:
            if move in ('n', 's'):
                direction.append(move+char)
                move = ''
            elif char in ('e', 'w'):
                direction.append(char)
            else:
                move = char
        directions.append(direction)
    return directions

def initialize_hex_tiles(directions):
    hex_tile = HexTile()
    for direction in directions:
        hex_tile.flip_tile(direction)
    hex_tile.surround_black_tiles()
    return hex_tile

def simulate_hex_tiles(hex_tiles):
    for n in range(100):
        hex_tiles.artistic_flip()
        hex_tiles.surround_black_tiles()

directions = parse_input()
hex_tiles = initialize_hex_tiles(directions)
print(hex_tiles.black_count)
simulate_hex_tiles(hex_tiles)
print(hex_tiles.black_count)

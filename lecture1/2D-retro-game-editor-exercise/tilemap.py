"""Grid-based tile map data structure with JSON save/load support."""

import json
import os

import pygame

from . import config

EMPTY = -1


class TileMap:
    """A 2D grid of tile indices. ``EMPTY`` marks an empty cell."""

    def __init__(self, width, height, tile_size):
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.tiles = [[EMPTY for _ in range(width)] for _ in range(height)]

    def set_tile(self, x, y, index):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.tiles[y][x] = index

    def get_tile(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return None

    def clear(self):
        self.tiles = [[EMPTY for _ in range(self.width)] for _ in range(self.height)]

    def to_dict(self):
        return {
            "width": self.width,
            "height": self.height,
            "tile_size": self.tile_size,
            "tiles": self.tiles,
        }

    @classmethod
    def from_dict(cls, data):
        tile_map = cls(data["width"], data["height"], data["tile_size"])
        tile_map.tiles = data["tiles"]
        return tile_map

    def save(self, path):
        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)

    def draw(self, surface, tileset, origin=(0, 0)):
        ox, oy = origin
        ts = self.tile_size

        for y in range(self.height):
            for x in range(self.width):
                index = self.tiles[y][x]
                cell_rect = (ox + x * ts, oy + y * ts, ts, ts)
                if index != EMPTY:
                    tile_image = tileset.get(index)
                    if tile_image is not None:
                        surface.blit(tile_image, cell_rect[:2])
                pygame.draw.rect(surface, config.COLOR_GRID_LINE, cell_rect, 1)

"""Loads a tileset image and slices it into individual tile surfaces.

If no tileset image exists yet, a small retro-style pixel-art tileset is
generated procedurally and saved to disk, so the editor works out of the box.
"""

import os
import pygame

# Each tile is described as an 8x8 grid of characters, scaled up to fill a
# TILE_SIZE x TILE_SIZE surface. This keeps the generated art blocky/retro.
_TILE_DEFINITIONS = [
    {
        "name": "grass",
        "colors": {".": (58, 122, 48), "#": (72, 148, 60)},
        "grid": [
            "........",
            "..#.....",
            "........",
            ".....#..",
            "........",
            "..#.....",
            "........",
            ".....#..",
        ],
    },
    {
        "name": "dirt",
        "colors": {".": (110, 78, 48), "#": (90, 62, 36)},
        "grid": [
            "........",
            ".#......",
            "......#.",
            "........",
            "...#....",
            "........",
            ".#....#.",
            "........",
        ],
    },
    {
        "name": "water",
        "colors": {".": (40, 90, 168), "#": (70, 130, 210)},
        "grid": [
            "........",
            "###.###.",
            "........",
            "..###.##",
            "........",
            "###.###.",
            "........",
            "..###.##",
        ],
    },
    {
        "name": "sand",
        "colors": {".": (214, 194, 130), "#": (196, 174, 108)},
        "grid": [
            "........",
            "..#.....",
            "........",
            ".....#..",
            "..#.....",
            "........",
            ".....#..",
            "........",
        ],
    },
    {
        "name": "stone",
        "colors": {".": (120, 120, 128), "#": (96, 96, 104)},
        "grid": [
            "########",
            "#......#",
            "#......#",
            "########",
            "#......#",
            "#......#",
            "########",
            "########",
        ],
    },
    {
        "name": "brick",
        "colors": {".": (150, 60, 50), "#": (100, 40, 34)},
        "grid": [
            "########",
            "..#..#..",
            "..#..#..",
            "########",
            "#..#..#.",
            "#..#..#.",
            "########",
            "..#..#..",
        ],
    },
    {
        "name": "path",
        "colors": {".": (176, 158, 128), "#": (150, 132, 104)},
        "grid": [
            "........",
            "..##....",
            "........",
            "....##..",
            "........",
            "..##....",
            "........",
            "....##..",
        ],
    },
    {
        "name": "tree",
        "colors": {
            ".": (58, 122, 48),
            "#": (34, 90, 34),
            "@": (94, 62, 34),
        },
        "grid": [
            "..###...",
            ".#####..",
            "#######.",
            ".#####..",
            "..###...",
            "...@....",
            "...@....",
            "........",
        ],
    },
    {
        "name": "bush",
        "colors": {".": (58, 122, 48), "#": (40, 100, 40)},
        "grid": [
            "........",
            "..###...",
            ".#####..",
            "#######.",
            ".#####..",
            "..###...",
            "........",
            "........",
        ],
    },
    {
        "name": "flower",
        "colors": {".": (58, 122, 48), "#": (72, 148, 60), "o": (230, 200, 60)},
        "grid": [
            "........",
            "...o....",
            "........",
            "........",
            "....o...",
            "........",
            "...o....",
            "........",
        ],
    },
]


class Tileset:
    """Holds a list of tile surfaces sliced from a tileset image."""

    def __init__(self, path, tile_size):
        self.path = path
        self.tile_size = tile_size
        self.tiles = []
        self.names = []
        self._load_or_create()

    def _load_or_create(self):
        if not os.path.exists(self.path):
            self._create_default_tileset()

        sheet = pygame.image.load(self.path).convert_alpha()
        cols = sheet.get_width() // self.tile_size
        rows = sheet.get_height() // self.tile_size

        for row in range(rows):
            for col in range(cols):
                rect = pygame.Rect(
                    col * self.tile_size,
                    row * self.tile_size,
                    self.tile_size,
                    self.tile_size,
                )
                self.tiles.append(sheet.subsurface(rect).copy())

        if not self.names:
            self.names = [d["name"] for d in _TILE_DEFINITIONS[: len(self.tiles)]]
            while len(self.names) < len(self.tiles):
                self.names.append(f"tile {len(self.names)}")

    def _create_default_tileset(self):
        directory = os.path.dirname(self.path)
        if directory:
            os.makedirs(directory, exist_ok=True)

        ts = self.tile_size
        sheet = pygame.Surface((ts * len(_TILE_DEFINITIONS), ts), pygame.SRCALPHA)

        for i, definition in enumerate(_TILE_DEFINITIONS):
            tile_surface = self._render_tile(definition, ts)
            sheet.blit(tile_surface, (i * ts, 0))

        pygame.image.save(sheet, self.path)

    @staticmethod
    def _render_tile(definition, tile_size):
        grid = definition["grid"]
        colors = definition["colors"]
        cells = len(grid)
        cell_size = max(1, tile_size // cells)

        surface = pygame.Surface((tile_size, tile_size))
        surface.fill(colors["."])

        for y, row in enumerate(grid):
            for x, char in enumerate(row):
                color = colors.get(char)
                if color is None:
                    continue
                rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
                pygame.draw.rect(surface, color, rect)

        return surface

    def get(self, index):
        if 0 <= index < len(self.tiles):
            return self.tiles[index]
        return None

    def name_of(self, index):
        if 0 <= index < len(self.names):
            return self.names[index]
        return "?"

    def count(self):
        return len(self.tiles)

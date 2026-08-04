"""Central configuration for the 2D retro tile map editor."""

TILE_SIZE = 32          # pixels per tile, both in the canvas and the tileset image
GRID_COLS = 20          # map width in tiles
GRID_ROWS = 15          # map height in tiles

CANVAS_WIDTH = GRID_COLS * TILE_SIZE
CANVAS_HEIGHT = GRID_ROWS * TILE_SIZE

PALETTE_WIDTH = 140
PALETTE_TILE_SIZE = 40
PALETTE_PADDING = 8

TOOLBAR_HEIGHT = 56

WINDOW_WIDTH = CANVAS_WIDTH + PALETTE_WIDTH
WINDOW_HEIGHT = CANVAS_HEIGHT + TOOLBAR_HEIGHT

FPS = 60

TILESET_PATH = "assets/tileset.png"
DEFAULT_MAP_PATH = "maps/level.json"

# Colors
COLOR_BG = (18, 18, 24)
COLOR_TOOLBAR_BG = (30, 30, 40)
COLOR_PALETTE_BG = (24, 24, 32)
COLOR_GRID_LINE = (60, 60, 70)
COLOR_TEXT = (230, 230, 230)
COLOR_SELECTED_BORDER = (255, 215, 0)
COLOR_ERASER_SLOT = (50, 50, 60)

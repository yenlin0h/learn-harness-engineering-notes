"""Main application loop for the 2D retro tile map editor."""

import pygame

from . import config
from .tilemap import EMPTY, TileMap
from .tileset import Tileset


class Editor:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Retro Tile Map Editor")
        self.screen = pygame.display.set_mode(
            (config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        )
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 16)
        self.small_font = pygame.font.SysFont("consolas", 13)

        self.tileset = Tileset(config.TILESET_PATH, config.TILE_SIZE)

        try:
            self.tile_map = TileMap.load(config.DEFAULT_MAP_PATH)
        except (FileNotFoundError, ValueError, KeyError):
            self.tile_map = TileMap(
                config.GRID_COLS, config.GRID_ROWS, config.TILE_SIZE
            )

        self.selected_tile = 0
        self.dirty = False
        self.running = True
        self.status_message = "Ready"

        self.canvas_origin = (0, config.TOOLBAR_HEIGHT)
        self.palette_origin = (config.CANVAS_WIDTH, config.TOOLBAR_HEIGHT)

    def run(self):
        while self.running:
            self._handle_events()
            self._draw()
            self.clock.tick(config.FPS)
        pygame.quit()

    # -- event handling -----------------------------------------------

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse(event.pos, event.button)
            elif event.type == pygame.MOUSEMOTION:
                buttons = pygame.mouse.get_pressed()
                if buttons[0]:
                    self._handle_mouse(event.pos, 1)
                elif buttons[2]:
                    self._handle_mouse(event.pos, 3)

    def _handle_keydown(self, event):
        mods = pygame.key.get_mods()
        ctrl_held = mods & pygame.KMOD_CTRL

        if ctrl_held and event.key == pygame.K_s:
            self.tile_map.save(config.DEFAULT_MAP_PATH)
            self.dirty = False
            self.status_message = f"Saved to {config.DEFAULT_MAP_PATH}"
        elif ctrl_held and event.key == pygame.K_o:
            try:
                self.tile_map = TileMap.load(config.DEFAULT_MAP_PATH)
                self.dirty = False
                self.status_message = f"Loaded {config.DEFAULT_MAP_PATH}"
            except (FileNotFoundError, ValueError, KeyError):
                self.status_message = f"No file found at {config.DEFAULT_MAP_PATH}"
        elif ctrl_held and event.key == pygame.K_n:
            self.tile_map.clear()
            self.dirty = True
            self.status_message = "Cleared map"
        elif event.key == pygame.K_ESCAPE:
            self.running = False
        elif event.key == pygame.K_e:
            self.selected_tile = EMPTY
        elif pygame.K_0 <= event.key <= pygame.K_9:
            digit = event.key - pygame.K_0
            index = 9 if digit == 0 else digit - 1
            if index < self.tileset.count():
                self.selected_tile = index

    def _handle_mouse(self, pos, button):
        if self._point_in_palette(pos):
            if button == 1:
                self._select_tile_at(pos)
            return

        if self._point_in_canvas(pos):
            cell = self._canvas_cell_at(pos)
            if cell is None:
                return
            x, y = cell
            if button == 1:
                self.tile_map.set_tile(x, y, self.selected_tile)
                self.dirty = True
            elif button == 3:
                self.tile_map.set_tile(x, y, EMPTY)
                self.dirty = True

    def _point_in_canvas(self, pos):
        ox, oy = self.canvas_origin
        x, y = pos
        return ox <= x < ox + config.CANVAS_WIDTH and oy <= y < oy + config.CANVAS_HEIGHT

    def _point_in_palette(self, pos):
        ox, oy = self.palette_origin
        x, y = pos
        return ox <= x < ox + config.PALETTE_WIDTH and oy <= y < oy + config.CANVAS_HEIGHT

    def _canvas_cell_at(self, pos):
        ox, oy = self.canvas_origin
        x, y = pos
        col = (x - ox) // config.TILE_SIZE
        row = (y - oy) // config.TILE_SIZE
        if 0 <= col < self.tile_map.width and 0 <= row < self.tile_map.height:
            return col, row
        return None

    def _select_tile_at(self, pos):
        ox, oy = self.palette_origin
        _, y = pos
        slot_height = config.PALETTE_TILE_SIZE + config.PALETTE_PADDING
        slot_index = (y - oy - config.PALETTE_PADDING) // slot_height
        if slot_index == 0:
            self.selected_tile = EMPTY
        else:
            tile_index = slot_index - 1
            if 0 <= tile_index < self.tileset.count():
                self.selected_tile = tile_index

    # -- drawing --------------------------------------------------------

    def _draw(self):
        self.screen.fill(config.COLOR_BG)
        self._draw_toolbar()
        self.tile_map.draw(self.screen, self.tileset, self.canvas_origin)
        self._draw_palette()
        pygame.display.flip()

    def _draw_toolbar(self):
        rect = (0, 0, config.WINDOW_WIDTH, config.TOOLBAR_HEIGHT)
        pygame.draw.rect(self.screen, config.COLOR_TOOLBAR_BG, rect)

        tool_name = "Eraser" if self.selected_tile == EMPTY else self.tileset.name_of(
            self.selected_tile
        )
        unsaved = " *unsaved*" if self.dirty else ""
        line1 = f"Tool: {tool_name}   File: {config.DEFAULT_MAP_PATH}{unsaved}   {self.status_message}"
        line2 = "LMB paint  RMB erase  1-9/0 pick tile  E eraser  Ctrl+S save  Ctrl+O load  Ctrl+N new  Esc quit"

        self.screen.blit(self.font.render(line1, True, config.COLOR_TEXT), (10, 6))
        self.screen.blit(self.small_font.render(line2, True, config.COLOR_TEXT), (10, 28))

    def _draw_palette(self):
        rect = (
            self.palette_origin[0],
            self.palette_origin[1],
            config.PALETTE_WIDTH,
            config.CANVAS_HEIGHT,
        )
        pygame.draw.rect(self.screen, config.COLOR_PALETTE_BG, rect)

        ox, oy = self.palette_origin
        slot_size = config.PALETTE_TILE_SIZE
        padding = config.PALETTE_PADDING

        # Eraser slot at the top.
        eraser_rect = pygame.Rect(ox + padding, oy + padding, slot_size, slot_size)
        pygame.draw.rect(self.screen, config.COLOR_ERASER_SLOT, eraser_rect)
        pygame.draw.line(
            self.screen, config.COLOR_TEXT, eraser_rect.topleft, eraser_rect.bottomright, 2
        )
        pygame.draw.line(
            self.screen, config.COLOR_TEXT, eraser_rect.topright, eraser_rect.bottomleft, 2
        )
        if self.selected_tile == EMPTY:
            pygame.draw.rect(self.screen, config.COLOR_SELECTED_BORDER, eraser_rect, 3)

        for index in range(self.tileset.count()):
            slot_y = oy + padding + (index + 1) * (slot_size + padding)
            tile_rect = pygame.Rect(ox + padding, slot_y, slot_size, slot_size)
            tile_image = pygame.transform.scale(
                self.tileset.get(index), (slot_size, slot_size)
            )
            self.screen.blit(tile_image, tile_rect.topleft)
            if index == self.selected_tile:
                pygame.draw.rect(self.screen, config.COLOR_SELECTED_BORDER, tile_rect, 3)
            else:
                pygame.draw.rect(self.screen, config.COLOR_GRID_LINE, tile_rect, 1)

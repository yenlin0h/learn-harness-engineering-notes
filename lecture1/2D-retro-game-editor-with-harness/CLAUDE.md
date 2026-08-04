# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Project

A 2D retro tile map editor built with Python + pygame. Tiles are procedurally
generated as pixel art on first run (no external art assets required).

## Setup & Run

```powershell
# create/activate venv (already exists as .venv)
.venv\Scripts\Activate.ps1

# install deps
pip install -r requirements.txt

# run the editor
python main.py
```

## Architecture

- `main.py` — entry point, constructs and runs `Editor`.
- `editor/config.py` — all constants (window size, tile size, colors, file paths).
- `editor/tileset.py` — `Tileset` loads `assets/tileset.png`; auto-generates it
  from hardcoded pixel patterns if missing.
- `editor/tilemap.py` — `TileMap` holds the 2D grid of tile indices (`-1` =
  empty) and handles JSON save/load (`maps/level.json`) and drawing.
- `editor/app.py` — `Editor` class: pygame event loop, mouse/keyboard input,
  toolbar + palette UI rendering.

## Controls

- Left click/drag on canvas: paint selected tile
- Right click/drag on canvas: erase
- Click palette on the right: select tile (top slot = eraser)
- `1`-`9`, `0`: quick-select tile by number; `E`: eraser
- `Ctrl+S` save, `Ctrl+O` load, `Ctrl+N` clear map, `Esc` quit

## Conventions

- Keep new tile types added to `_TILE_DEFINITIONS` in `editor/tileset.py` as
  8x8 character grids (see existing entries for the pattern).
- Map files are plain JSON: `{width, height, tile_size, tiles}`.
- No test suite yet — verify changes with a quick manual run, or a headless
  smoke test using `SDL_VIDEODRIVER=dummy` if a display isn't available.

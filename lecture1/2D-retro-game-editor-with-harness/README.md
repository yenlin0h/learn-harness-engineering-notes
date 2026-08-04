# 🎮 2D Retro Game Editor — With Harness

> **Run 2 of Lecture 01 Exercise 1: Harness Engineering**
> The same task as Run 1, but this time with a proper harness in place.

---

## 📋 Overview

A 2D tile-based retro game editor built with Python + pygame, scaffolded
and verified using a full harness — CLAUDE.md, a pre-defined test suite,
explicit verification commands, and a clear Definition of Done.

---

## 🚀 Quick Start

```powershell
# Install dependencies
pip install -r requirements.txt

# Run all tests
python -m pytest -v

# Launch the editor
python main.py
```

---

## 🕹️ Editor Controls

| Input | Action |
|-------|--------|
| `Left Click` / drag | Paint selected tile |
| `Right Click` / drag | Erase tile |
| `1` – `9`, `0` | Quick-select tile from palette |
| `E` | Toggle eraser |
| `Ctrl + S` | Save map to JSON |
| `Ctrl + O` | Load map from JSON |
| `Ctrl + N` | New / clear map |
| `Escape` | Quit |

---

## 📁 Project Structure

```
2D-retro-game-editor-with-harness/
├── __init__.py
├── app.py          ← main editor loop
├── config.py       ← all sizing/color constants
├── tilemap.py      ← grid data model with JSON save/load
├── tileset.py      ← auto-generates retro pixel-art tileset
├── conftest.py     ← headless SDL setup for all tests
├── test_tilemap.py ← grid bounds, clear, save/load roundtrips
├── test_tileset.py ← tileset generation, caching, lookups
├──  test_app_smoke.py ← full Editor paint/erase/save/load/quit
├── maps/               ← saved map JSON files land here
├── assets/             ← tileset.png auto-generated on first run
├── main.py             ← entry point
├── pytest.ini          ← testpaths and pythonpath configured
├── requirements.txt
├── CLAUDE.md
└── .gitignore
```

---

## 🧱 Tile Palette

| Key | Tile |
|-----|------|
| `1` | 🟩 Grass |
| `2` | 🟫 Dirt |
| `3` | 🟦 Water |
| `4` | 🟨 Sand |
| `5` | ⬜ Stone |
| `6` | 🟥 Brick |
| `7` | ⬛ Path |
| `8` | 🌲 Tree |
| `9` | 🌿 Bush |
| `0` | 🌸 Flower |

---

## ✅ Verification

All verification commands must pass before any task is declared done:

```powershell
# Run the full test suite (32 tests)
python -m pytest -v

# Launch and manually verify the editor window
python main.py
```

### Test Coverage

| Test File | What It Covers |
|-----------|---------------|
| `test_tilemap.py` | Grid bounds, set/get tile, clear, JSON save/load roundtrip |
| `test_tileset.py` | Auto-generation, caching, tile count, lookup by index |
| `test_app_smoke.py` | Full `Editor` — paint, erase, save, load, quit, one full `run()` iteration |

### Test Results

```
32 passed in 0.00s ✅
```

---

## 🐛 Bug Caught by Harness

> `Editor._handle_keydown` was checking `pygame.key.get_mods()`
> (live SDL keyboard state) instead of the event's `.mod` attribute.
>
> - ✅ Correct for real interactive usage
> - ❌ Breaks synthetic `KEYDOWN` events in tests
>
> **Fix:** `conftest.py` patches `pygame.key.get_mods` so synthetic
> events behave correctly in the test environment.
>
> **This bug was invisible in Run 1. The harness caught it in Run 2.**

---

## 🛡️ Harness Components

### `AGENTS.md`
Defines the tech stack, architecture conventions, coordinate system
(`col, row` — never `x, y`), JSON envelope format, and the
explicit Definition of Done that the agent must satisfy.

### `conftest.py`
Forces `SDL_VIDEODRIVER=dummy` and `SDL_AUDIODRIVER=dummy` before
any test runs, initializes a headless pygame display, and tears it
down cleanly after the session — so all 32 tests run without a
real screen.

### `pytest.ini`
```ini
[pytest]
testpaths = tests
pythonpath = .
```
Ensures `editor.*` imports resolve correctly from the project root.

---

## 📊 Harness Impact (vs Run 1)

| Metric | Run 1 — No Harness | Run 2 — With Harness |
|--------|-------------------|---------------------|
| Tests before task | 0 | 3 test files + conftest |
| Tests after task | 2 inline smoke checks | **32 passing tests** |
| Verification gap | **100%** | **0%** |
| Env setup failures | 2 | 0 |
| Real bugs caught | 0 | **1** |
| Cross-session continuity | ❌ | ✅ CLAUDE.md |

"""Unit tests for editor.tilemap.TileMap."""

import json

import pytest

from editor.tilemap import EMPTY, TileMap


def test_new_tilemap_is_all_empty():
    tile_map = TileMap(width=4, height=3, tile_size=32)
    assert tile_map.width == 4
    assert tile_map.height == 3
    assert all(cell == EMPTY for row in tile_map.tiles for cell in row)


def test_set_and_get_tile():
    tile_map = TileMap(width=4, height=3, tile_size=32)
    tile_map.set_tile(1, 2, 5)
    assert tile_map.get_tile(1, 2) == 5


@pytest.mark.parametrize(
    "x, y",
    [(-1, 0), (0, -1), (4, 0), (0, 3), (100, 100)],
)
def test_set_tile_out_of_bounds_is_ignored(x, y):
    tile_map = TileMap(width=4, height=3, tile_size=32)
    tile_map.set_tile(x, y, 5)
    # No exception raised, and no in-bounds cell was mutated.
    assert all(cell == EMPTY for row in tile_map.tiles for cell in row)


@pytest.mark.parametrize(
    "x, y",
    [(-1, 0), (0, -1), (4, 0), (0, 3), (100, 100)],
)
def test_get_tile_out_of_bounds_returns_none(x, y):
    tile_map = TileMap(width=4, height=3, tile_size=32)
    assert tile_map.get_tile(x, y) is None


def test_clear_resets_all_cells():
    tile_map = TileMap(width=4, height=3, tile_size=32)
    tile_map.set_tile(0, 0, 3)
    tile_map.set_tile(2, 1, 7)
    tile_map.clear()
    assert all(cell == EMPTY for row in tile_map.tiles for cell in row)


def test_to_dict_round_trip():
    tile_map = TileMap(width=2, height=2, tile_size=16)
    tile_map.set_tile(0, 0, 1)
    tile_map.set_tile(1, 1, 2)

    data = tile_map.to_dict()
    restored = TileMap.from_dict(data)

    assert restored.width == tile_map.width
    assert restored.height == tile_map.height
    assert restored.tile_size == tile_map.tile_size
    assert restored.tiles == tile_map.tiles


def test_save_creates_valid_json(tmp_path):
    tile_map = TileMap(width=3, height=2, tile_size=32)
    tile_map.set_tile(0, 0, 4)
    path = tmp_path / "maps" / "level.json"

    tile_map.save(str(path))

    assert path.exists()
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    assert data["width"] == 3
    assert data["height"] == 2
    assert data["tiles"][0][0] == 4


def test_save_then_load_round_trip(tmp_path):
    tile_map = TileMap(width=3, height=2, tile_size=32)
    tile_map.set_tile(0, 0, 4)
    tile_map.set_tile(2, 1, 9)
    path = tmp_path / "level.json"

    tile_map.save(str(path))
    loaded = TileMap.load(str(path))

    assert loaded.tiles == tile_map.tiles
    assert loaded.width == tile_map.width
    assert loaded.height == tile_map.height


def test_load_missing_file_raises_file_not_found(tmp_path):
    missing_path = tmp_path / "does_not_exist.json"
    with pytest.raises(FileNotFoundError):
        TileMap.load(str(missing_path))

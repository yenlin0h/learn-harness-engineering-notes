"""Unit tests for editor.tileset.Tileset."""

from editor.tileset import Tileset


def test_generates_default_tileset_file_when_missing(tmp_path):
    path = tmp_path / "assets" / "tileset.png"
    assert not path.exists()

    tileset = Tileset(str(path), tile_size=32)

    assert path.exists()
    assert tileset.count() > 0


def test_loads_existing_tileset_file_without_regenerating(tmp_path):
    path = tmp_path / "tileset.png"

    first = Tileset(str(path), tile_size=32)
    mtime_after_first = path.stat().st_mtime
    first_count = first.count()

    second = Tileset(str(path), tile_size=32)

    assert path.stat().st_mtime == mtime_after_first
    assert second.count() == first_count


def test_get_returns_surface_for_valid_index(tmp_path):
    tileset = Tileset(str(tmp_path / "tileset.png"), tile_size=32)
    tile = tileset.get(0)
    assert tile is not None
    assert tile.get_size() == (32, 32)


def test_get_returns_none_for_invalid_index(tmp_path):
    tileset = Tileset(str(tmp_path / "tileset.png"), tile_size=32)
    assert tileset.get(-1) is None
    assert tileset.get(tileset.count()) is None


def test_name_of_returns_placeholder_for_invalid_index(tmp_path):
    tileset = Tileset(str(tmp_path / "tileset.png"), tile_size=32)
    assert tileset.name_of(tileset.count() + 1) == "?"


def test_name_of_returns_known_names(tmp_path):
    tileset = Tileset(str(tmp_path / "tileset.png"), tile_size=32)
    assert tileset.name_of(0) == "grass"

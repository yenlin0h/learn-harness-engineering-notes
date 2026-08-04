"""Headless smoke tests that exercise the Editor application loop.

These do not open a real window (pygame runs against the SDL "dummy"
driver, configured in conftest.py) but they do drive real pygame Surface
and event objects through the full paint / erase / save / load code paths,
guarding against regressions that only show up when the app is "running".
"""

import pygame
import pytest

from editor import config
from editor.app import Editor
from editor.tilemap import EMPTY


@pytest.fixture
def editor(tmp_path, monkeypatch):
    """A fully constructed Editor pointed at a throwaway map/tileset path."""
    monkeypatch.setattr(config, "TILESET_PATH", str(tmp_path / "tileset.png"))
    monkeypatch.setattr(config, "DEFAULT_MAP_PATH", str(tmp_path / "level.json"))
    ed = Editor()
    yield ed
    try:
        pygame.event.clear()
    except pygame.error:
        pass  # the run-loop smoke test may have already quit pygame


def test_editor_starts_with_empty_map(editor):
    assert editor.running is True
    assert editor.dirty is False
    assert all(
        cell == EMPTY for row in editor.tile_map.tiles for cell in row
    )


def test_draw_does_not_raise(editor):
    editor._draw()


def test_paint_tile_via_mouse_click(editor):
    editor.selected_tile = 0
    canvas_x, canvas_y = editor.canvas_origin
    pos = (canvas_x + config.TILE_SIZE // 2, canvas_y + config.TILE_SIZE // 2)

    editor._handle_mouse(pos, button=1)

    assert editor.tile_map.get_tile(0, 0) == 0
    assert editor.dirty is True


def test_erase_tile_via_right_click(editor):
    editor.tile_map.set_tile(0, 0, 3)
    canvas_x, canvas_y = editor.canvas_origin
    pos = (canvas_x + config.TILE_SIZE // 2, canvas_y + config.TILE_SIZE // 2)

    editor._handle_mouse(pos, button=3)

    assert editor.tile_map.get_tile(0, 0) == EMPTY


def test_click_outside_canvas_and_palette_is_a_no_op(editor):
    editor._handle_mouse((-10, -10), button=1)
    assert editor.dirty is False


def test_escape_key_stops_the_loop(editor):
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, mod=0)
    editor._handle_keydown(event)
    assert editor.running is False


def test_ctrl_n_clears_the_map(editor, monkeypatch):
    # The app checks the live SDL modifier state (pygame.key.get_mods()),
    # not the synthetic event's .mod attribute, so it must be patched too.
    monkeypatch.setattr(pygame.key, "get_mods", lambda: pygame.KMOD_CTRL)
    editor.tile_map.set_tile(0, 0, 2)
    event = pygame.event.Event(
        pygame.KEYDOWN, key=pygame.K_n, mod=pygame.KMOD_CTRL
    )
    editor._handle_keydown(event)
    assert editor.tile_map.get_tile(0, 0) == EMPTY
    assert editor.dirty is True


def test_ctrl_s_then_ctrl_o_round_trips_the_map(editor, monkeypatch):
    monkeypatch.setattr(pygame.key, "get_mods", lambda: pygame.KMOD_CTRL)
    editor.tile_map.set_tile(1, 1, 4)

    save_event = pygame.event.Event(
        pygame.KEYDOWN, key=pygame.K_s, mod=pygame.KMOD_CTRL
    )
    editor._handle_keydown(save_event)
    assert editor.dirty is False

    editor.tile_map.set_tile(1, 1, EMPTY)

    load_event = pygame.event.Event(
        pygame.KEYDOWN, key=pygame.K_o, mod=pygame.KMOD_CTRL
    )
    editor._handle_keydown(load_event)

    assert editor.tile_map.get_tile(1, 1) == 4


def test_one_full_frame_via_run_loop(editor, monkeypatch):
    """Drive Editor.run() for exactly one iteration end-to-end."""
    quit_event = pygame.event.Event(pygame.QUIT)
    monkeypatch.setattr(pygame.event, "get", lambda: [quit_event])
    # Editor.run() calls pygame.quit() once the loop ends; avoid tearing
    # down the shared, session-wide headless display used by other tests.
    monkeypatch.setattr(pygame, "quit", lambda: None)

    editor.run()

    assert editor.running is False

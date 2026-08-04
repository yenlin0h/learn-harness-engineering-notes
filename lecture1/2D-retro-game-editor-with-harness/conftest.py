"""Shared pytest fixtures for the editor test harness.

All tests run headless: pygame is forced to use the SDL "dummy" video and
audio drivers so the full test suite works in CI, over SSH, or on any
machine without a display.
"""

import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame
import pytest


@pytest.fixture(scope="session", autouse=True)
def pygame_display():
    """Initialize a real (but headless) pygame display for the whole session.

    Several editor modules (Tileset, Editor) call ``.convert_alpha()`` /
    ``pygame.font`` APIs that require the display module to be initialized
    first, even when nothing is actually rendered to a screen.
    """
    pygame.init()
    pygame.display.set_mode((1, 1))
    yield
    pygame.quit()


@pytest.fixture
def tmp_asset_path(tmp_path):
    """A throwaway path (inside pytest's tmp_path) for tileset/map files."""
    return tmp_path

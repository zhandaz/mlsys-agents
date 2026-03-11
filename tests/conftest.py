"""Shared fixtures for mlsys_agents tests."""

import matplotlib

matplotlib.use("Agg")  # Non-interactive backend for CI

import pytest  # noqa: E402

from mlsys_agents.plot import Palette, reset_theme, set_theme  # noqa: E402


@pytest.fixture(autouse=True)
def _clean_theme():
    """Reset theme before each test to avoid cross-test contamination."""
    reset_theme()
    yield
    reset_theme()


@pytest.fixture()
def methods_palette():
    """Register a methods palette (LoRAFusion-style) and return its name."""
    pal = Palette(
        colors={"lora": "#2D6A4F", "full_ft": "#264653", "qlora": "#52B788", "adapter": "#E9C46A"},
        display_names={"lora": "LoRA", "full_ft": "Full Fine-Tune", "qlora": "QLoRA", "adapter": "Adapter"},
    )
    set_theme(palettes={"methods": pal})
    return "methods"


@pytest.fixture()
def tmp_output(tmp_path):
    """Return a temporary output directory."""
    return tmp_path / "figures"

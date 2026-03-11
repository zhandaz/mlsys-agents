"""Tests for common utilities: save, auto_figsize, color resolution."""

import matplotlib.pyplot as plt

from mlsys_agents.plot.common import auto_figsize, resolve_colors, resolve_display_names, save
from mlsys_agents.plot.theme import QUALITATIVE_10, Palette, set_theme


class TestSave:
    def test_saves_default_formats(self, tmp_output):
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3])
        paths = save(fig, tmp_output / "test_chart")
        assert len(paths) == 2
        assert paths[0].suffix == ".pdf"
        assert paths[1].suffix == ".png"
        assert all(p.exists() for p in paths)

    def test_saves_custom_formats(self, tmp_output):
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3])
        paths = save(fig, tmp_output / "test_chart", formats=["png"])
        assert len(paths) == 1
        assert paths[0].suffix == ".png"

    def test_close_by_default(self, tmp_output):
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3])
        save(fig, tmp_output / "test_chart")
        # After close, figure should not be in plt.get_fignums()
        assert fig.number not in plt.get_fignums()

    def test_no_close(self, tmp_output):
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3])
        save(fig, tmp_output / "test_chart", close=False)
        assert fig.number in plt.get_fignums()
        plt.close(fig)

    def test_creates_parent_dirs(self, tmp_output):
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3])
        paths = save(fig, tmp_output / "subdir" / "nested" / "chart")
        assert all(p.exists() for p in paths)


class TestAutoFigsize:
    def test_vertical_minimum(self):
        w, h = auto_figsize(3)
        assert w >= 6
        assert h == 4

    def test_vertical_scales(self):
        w1, _ = auto_figsize(3)
        w2, _ = auto_figsize(15)
        assert w2 > w1

    def test_horizontal(self):
        w, h = auto_figsize(10, "horizontal")
        assert w >= 6
        assert h >= 3


class TestResolveColors:
    def test_fallback_to_qualitative(self):
        colors = resolve_colors(["a", "b", "c"])
        assert colors == QUALITATIVE_10[:3]

    def test_explicit_dict(self):
        colors = resolve_colors(["a", "b"], colors={"a": "#111", "b": "#222"})
        assert colors == ["#111", "#222"]

    def test_explicit_list(self):
        colors = resolve_colors(["a", "b", "c"], colors=["#F00", "#0F0"])
        assert colors == ["#F00", "#0F0", "#F00"]  # cycles

    def test_palette_resolution(self):
        pal = Palette(colors={"lora": "#2D6A4F", "full_ft": "#264653"})
        set_theme(palettes={"methods": pal})
        colors = resolve_colors(["lora", "full_ft"], palette="methods")
        assert colors == ["#2D6A4F", "#264653"]

    def test_palette_missing_key_falls_back(self):
        pal = Palette(colors={"lora": "#2D6A4F"})
        set_theme(palettes={"methods": pal})
        colors = resolve_colors(["lora", "unknown"], palette="methods")
        assert colors[0] == "#2D6A4F"
        assert colors[1] == QUALITATIVE_10[1]  # fallback


class TestResolveDisplayNames:
    def test_no_palette(self):
        names = resolve_display_names(["lora", "full_ft"])
        assert names == ["lora", "full_ft"]

    def test_with_palette(self):
        pal = Palette(display_names={"lora": "LoRA", "full_ft": "Full FT"})
        set_theme(palettes={"methods": pal})
        names = resolve_display_names(["lora", "full_ft"], palette="methods")
        assert names == ["LoRA", "Full FT"]

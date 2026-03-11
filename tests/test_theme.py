"""Tests for theme and palette system."""

from mlsys_agents.plot.theme import Palette, Theme, get_theme, reset_theme, set_theme


class TestPalette:
    def test_color_registered(self):
        pal = Palette(colors={"lora": "#2D6A4F"})
        assert pal.color("lora") == "#2D6A4F"

    def test_color_fallback(self):
        pal = Palette(colors={})
        assert pal.color("unknown") == "#999999"
        assert pal.color("unknown", "#FF0000") == "#FF0000"

    def test_display_registered(self):
        pal = Palette(display_names={"lora": "LoRA"})
        assert pal.display("lora") == "LoRA"

    def test_display_passthrough(self):
        pal = Palette(display_names={})
        assert pal.display("lora") == "lora"


class TestTheme:
    def test_default_values(self):
        t = Theme()
        assert t.base_fontsize == 13
        assert t.dpi == 300
        assert t.formats == ["pdf", "png"]

    def test_derived_fontsizes(self):
        t = Theme(base_fontsize=20)
        assert t.tick_fontsize == 17.0
        assert t.value_fontsize == 14.0

    def test_resolve_palette_none(self):
        t = Theme()
        assert t.resolve_palette(None) is None
        assert t.resolve_palette("nonexistent") is None

    def test_resolve_palette_registered(self):
        pal = Palette(colors={"x": "#000"})
        t = Theme(palettes={"mypal": pal})
        assert t.resolve_palette("mypal") is pal


class TestSetTheme:
    def test_set_updates_fields(self):
        set_theme(base_fontsize=20, dpi=150)
        t = get_theme()
        assert t.base_fontsize == 20
        assert t.dpi == 150

    def test_set_preserves_unset_fields(self):
        set_theme(base_fontsize=20)
        t = get_theme()
        assert t.dpi == 300  # default preserved

    def test_set_merges_palettes(self):
        pal1 = Palette(colors={"a": "#111"})
        pal2 = Palette(colors={"b": "#222"})
        set_theme(palettes={"p1": pal1})
        set_theme(palettes={"p2": pal2})
        t = get_theme()
        assert t.resolve_palette("p1") is pal1
        assert t.resolve_palette("p2") is pal2

    def test_reset(self):
        set_theme(base_fontsize=99)
        t = reset_theme()
        assert t.base_fontsize == 13

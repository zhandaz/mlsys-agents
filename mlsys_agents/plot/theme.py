"""Visual theme configuration: palettes, font sizes, and defaults.

The theme is a module-level singleton set once and auto-resolved by all chart functions.
Register named palettes to map data keys to consistent colors and display names.

Example::

    from mlsys_agents.plot import Palette, set_theme

    methods = Palette(
        colors={"lora": "#2D6A4F", "full_ft": "#264653"},
        display_names={"lora": "LoRA", "full_ft": "Full Fine-Tune"},
    )
    set_theme(palettes={"methods": methods}, base_fontsize=12)
"""

from __future__ import annotations

from dataclasses import dataclass, field

import matplotlib as mpl

# ACM/IEEE/USENIX-safe: embed fonts as Type 42 (TrueType)
mpl.rcParams["pdf.fonttype"] = 42
mpl.rcParams["ps.fonttype"] = 42
mpl.rcParams["font.family"] = "DejaVu Sans"

# 10-color qualitative fallback (Tol-inspired, colorblind-safe)
QUALITATIVE_10: list[str] = [
    "#264653",
    "#2A9D8F",
    "#E9C46A",
    "#F4A261",
    "#E76F51",
    "#1B4332",
    "#2D6A4F",
    "#40916C",
    "#52B788",
    "#74C69D",
]


@dataclass
class Palette:
    """Named color mapping for semantic data keys.

    Args:
        colors: Maps data keys to hex colors (e.g., ``{"lora": "#2D6A4F"}``).
        display_names: Maps data keys to human-readable labels
            (e.g., ``{"lora": "LoRA"}``). Keys not present are displayed as-is.
    """

    colors: dict[str, str] = field(default_factory=dict)
    display_names: dict[str, str] = field(default_factory=dict)

    def color(self, key: str, fallback: str = "#999999") -> str:
        """Return the hex color for *key*, or *fallback* if unregistered."""
        return self.colors.get(key, fallback)

    def display(self, key: str) -> str:
        """Return the display name for *key*, or *key* itself if unregistered."""
        return self.display_names.get(key, key)


@dataclass
class Theme:
    """Global visual configuration resolved by every chart function.

    Attributes:
        palettes: Named palette registry (resolved by ``palette="name"`` kwarg).
        base_fontsize: Reference size. Axis labels use this directly; tick labels
            use 85%, value labels 70%.
        dpi: Resolution for rasterized outputs.
        formats: Default file formats for :func:`~mlsys_agents.plot.common.save`.
        edge_color: Default bar/patch edge color.
        edge_width: Default bar/patch edge width.
        grid_alpha: Default grid line opacity.
    """

    palettes: dict[str, Palette] = field(default_factory=dict)
    base_fontsize: float = 13
    dpi: int = 300
    formats: list[str] = field(default_factory=lambda: ["pdf", "png"])
    edge_color: str = "black"
    edge_width: float = 0.5
    grid_alpha: float = 0.3

    @property
    def tick_fontsize(self) -> float:
        """Tick label font size (85% of base)."""
        return self.base_fontsize * 0.85

    @property
    def value_fontsize(self) -> float:
        """Value annotation font size (70% of base)."""
        return self.base_fontsize * 0.70

    def resolve_palette(self, name: str | None) -> Palette | None:
        """Look up a palette by name, returning ``None`` if not found."""
        if name is None:
            return None
        return self.palettes.get(name)


# Module-level singleton
_current_theme = Theme()


def get_theme() -> Theme:
    """Return the current global theme."""
    return _current_theme


def set_theme(
    *,
    palettes: dict[str, Palette] | None = None,
    base_fontsize: float | None = None,
    dpi: int | None = None,
    formats: list[str] | None = None,
    edge_color: str | None = None,
    edge_width: float | None = None,
    grid_alpha: float | None = None,
) -> Theme:
    """Update the global theme in-place and return it.

    Only provided fields are updated; others retain their current values.

    Example::

        set_theme(base_fontsize=14, dpi=150)
    """
    t = _current_theme
    if palettes is not None:
        t.palettes.update(palettes)
    if base_fontsize is not None:
        t.base_fontsize = base_fontsize
    if dpi is not None:
        t.dpi = dpi
    if formats is not None:
        t.formats = formats
    if edge_color is not None:
        t.edge_color = edge_color
    if edge_width is not None:
        t.edge_width = edge_width
    if grid_alpha is not None:
        t.grid_alpha = grid_alpha
    return t


def reset_theme() -> Theme:
    """Reset the global theme to defaults and return the new instance."""
    global _current_theme  # noqa: PLW0603
    _current_theme = Theme()
    return _current_theme

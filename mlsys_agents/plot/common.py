"""Shared utilities: save, auto_figsize, grid setup, color resolution.

These are internal plumbing used by all chart functions, plus the public
:func:`save` and :func:`auto_figsize` helpers.
"""

from __future__ import annotations

from itertools import chain
from pathlib import Path
from typing import TYPE_CHECKING, Literal

from matplotlib import pyplot as plt

from mlsys_agents.plot.theme import QUALITATIVE_10, get_theme

if TYPE_CHECKING:
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure

# Z-order layers (lower = further back)
ZORDER_GRID = 0
ZORDER_BARS = 3
ZORDER_LINES = 3
ZORDER_MARKERS = 4
ZORDER_AXIS = 5
ZORDER_LABELS = 7


def save(
    fig: Figure,
    path: str | Path,
    *,
    formats: list[str] | None = None,
    close: bool = True,
    dpi: int | None = None,
) -> list[Path]:
    """Save a figure to one or more formats, then close it by default.

    Args:
        fig: Matplotlib figure to save.
        path: Output path without extension (e.g., ``"figures/bar_chart"``).
        formats: File formats (default from theme, typically ``["pdf", "png"]``).
        close: Whether to close the figure after saving (default ``True``).
        dpi: Resolution override (default from theme).

    Returns:
        List of saved file paths.
    """
    theme = get_theme()
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if formats is None:
        formats = theme.formats
    if dpi is None:
        dpi = theme.dpi

    saved: list[Path] = []
    for fmt in formats:
        out = path.with_suffix(f".{fmt}")
        fig.savefig(out, bbox_inches="tight", dpi=dpi)
        saved.append(out)

    if close:
        plt.close(fig)
    return saved


def auto_figsize(n: int, orientation: str = "vertical") -> tuple[float, float]:
    """Compute a reasonable figure size from the number of data items.

    Args:
        n: Number of bars, categories, or data points.
        orientation: ``"vertical"`` or ``"horizontal"``.

    Returns:
        ``(width, height)`` tuple in inches.
    """
    if orientation == "horizontal":
        return (max(6, n * 0.8), max(3, n * 0.5))
    return (max(6, n * 1.0), 4)


# ------------------------------------------------------------------
# Internal helpers used by chart modules
# ------------------------------------------------------------------


def setup_grid(ax: Axes, orientation: str = "vertical") -> None:
    """Apply default grid styling and spine z-order to an axes."""
    theme = get_theme()
    grid_axis = "x" if orientation == "horizontal" else "y"
    ax.grid(axis=grid_axis, linestyle="--", alpha=theme.grid_alpha, color="black", linewidth=0.5, zorder=ZORDER_GRID)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_zorder(ZORDER_AXIS)


def set_labels(
    ax: Axes,
    *,
    xlabel: str | None = None,
    ylabel: str | None = None,
    title: str | None = None,
) -> None:
    """Apply axis labels and title with theme font sizes."""
    theme = get_theme()
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=theme.base_fontsize)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=theme.base_fontsize)
    if title:
        ax.set_title(title, fontsize=theme.base_fontsize + 2)


def tick_rotation(n: int, *, threshold: int = 5, angle: int = 30) -> tuple[int, str]:
    """Compute tick label rotation and horizontal alignment.

    Returns:
        ``(rotation_degrees, horizontal_alignment)`` tuple.
    """
    rotation = angle if n > threshold else 0
    ha = "right" if rotation else "center"
    return rotation, ha


def unique_inner_keys(nested: dict[str, dict]) -> list[str]:
    """Collect unique keys from nested dicts, preserving first-seen order."""
    return list(dict.fromkeys(chain.from_iterable(d.keys() for d in nested.values())))


def finalize(fig: Figure, *, owns_figure: bool) -> None:
    """Apply tight_layout only when the library created the figure."""
    if owns_figure:
        fig.tight_layout()


def resolve_colors(
    keys: list[str],
    *,
    palette: str | None = None,
    colors: dict[str, str] | list[str] | None = None,
) -> list[str]:
    """Resolve colors for a list of data keys.

    Priority: explicit ``colors`` > registered ``palette`` > qualitative fallback.

    Args:
        keys: Data keys to resolve colors for.
        palette: Name of a registered palette in the current theme.
        colors: Explicit color mapping (dict) or list. Overrides palette.

    Returns:
        List of hex color strings, one per key.
    """
    if colors is not None:
        if isinstance(colors, dict):
            return [colors.get(k, QUALITATIVE_10[i % len(QUALITATIVE_10)]) for i, k in enumerate(keys)]
        return [colors[i % len(colors)] for i in range(len(keys))]

    theme = get_theme()
    pal = theme.resolve_palette(palette)
    if pal is not None:
        return [pal.color(k, QUALITATIVE_10[i % len(QUALITATIVE_10)]) for i, k in enumerate(keys)]

    return [QUALITATIVE_10[i % len(QUALITATIVE_10)] for i in range(len(keys))]


def resolve_display_names(keys: list[str], *, palette: str | None = None) -> list[str]:
    """Resolve display names for a list of data keys.

    Args:
        keys: Data keys to resolve display names for.
        palette: Name of a registered palette in the current theme.

    Returns:
        List of display name strings, one per key.
    """
    theme = get_theme()
    pal = theme.resolve_palette(palette)
    if pal is not None:
        return [pal.display(k) for k in keys]
    return list(keys)


def make_fig_ax(
    figsize: tuple[float, float],
    ax: Axes | None,
) -> tuple[Figure, Axes, bool]:
    """Create or reuse a Figure/Axes pair.

    Args:
        figsize: Resolved figure size (used only when creating a new figure).
        ax: Optional existing axes to reuse.

    Returns:
        ``(fig, ax, owns_figure)`` where *owns_figure* is ``True`` when a new
        figure was created (so the caller knows whether to call tight_layout).
    """
    if ax is not None:
        return ax.figure, ax, False
    theme = get_theme()
    fig, new_ax = plt.subplots(figsize=figsize, dpi=theme.dpi)
    return fig, new_ax, True


# Keep old name for backwards compat within this package
_make_fig_ax = make_fig_ax

Orientation = Literal["vertical", "horizontal"]
"""Type alias for orientation parameters."""

SortOrder = Literal["descending", "ascending"]
"""Type alias for sort order parameters."""

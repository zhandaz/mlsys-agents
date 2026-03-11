"""Stacked bar chart: segments stacked within each bar.

Example::

    from mlsys_agents.plot import stacked_bar, save

    data = {
        "LLaMA-7B": {"compute": 0.6, "io": 0.25, "idle": 0.15},
        "LLaMA-13B": {"compute": 0.7, "io": 0.2, "idle": 0.1},
    }
    fig, ax = stacked_bar(data, ylabel="Time (normalized)")
    save(fig, "time_breakdown")
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

from mlsys_agents.plot.common import (
    ZORDER_BARS,
    ZORDER_LABELS,
    Orientation,
    auto_figsize,
    finalize,
    make_fig_ax,
    resolve_colors,
    resolve_display_names,
    set_labels,
    setup_grid,
    tick_rotation,
    unique_inner_keys,
)
from mlsys_agents.plot.theme import get_theme

if TYPE_CHECKING:
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure


def stacked_bar(
    data: dict[str, dict[str, float]],
    *,
    ylabel: str | None = None,
    xlabel: str | None = None,
    title: str | None = None,
    orientation: Orientation = "vertical",
    show_values: bool = False,
    value_fmt: str = ".0f",
    palette: str | None = None,
    colors: dict[str, str] | list[str] | None = None,
    figsize: tuple[float, float] | None = None,
    ax: Axes | None = None,
) -> tuple[Figure, Axes]:
    """Create a stacked bar chart.

    Args:
        data: ``{bar_label: {segment: value}}``. Segments are stacked within
            each bar in the order they first appear.
        ylabel: Y-axis label.
        xlabel: X-axis label.
        title: Figure title.
        orientation: ``"vertical"`` (default) or ``"horizontal"``.
        show_values: Annotate non-zero segments with their value.
        value_fmt: Format string for value annotations.
        palette: Name of a registered palette (resolves segment keys).
        colors: Explicit colors per segment. Overrides *palette*.
        figsize: Figure size in inches. Auto-computed if omitted.
        ax: Existing axes to draw on.

    Returns:
        ``(Figure, Axes)`` tuple.
    """
    if not data:
        msg = "No data to plot"
        raise ValueError(msg)

    bar_labels = list(data.keys())
    segments = unique_inner_keys(data)

    n_bars = len(bar_labels)
    theme = get_theme()
    color_list = resolve_colors(segments, palette=palette, colors=colors)
    segment_display = resolve_display_names(segments, palette=palette)

    horiz = orientation == "horizontal"
    fig, ax_, owns = make_fig_ax(figsize or auto_figsize(n_bars, orientation), ax)

    positions = np.arange(n_bars)
    bottom = np.zeros(n_bars)
    bar_width = 0.6

    for i, segment in enumerate(segments):
        values = np.array([data[b].get(segment, 0) for b in bar_labels], dtype=float)

        bar_kw: dict[str, Any] = {
            "color": color_list[i],
            "edgecolor": theme.edge_color,
            "linewidth": theme.edge_width,
            "zorder": ZORDER_BARS,
        }

        if horiz:
            container = ax_.barh(positions, values, height=bar_width, left=bottom, label=segment_display[i], **bar_kw)
        else:
            container = ax_.bar(positions, values, width=bar_width, bottom=bottom, label=segment_display[i], **bar_kw)

        if show_values:
            labels = [format(v, value_fmt) if v > 0 else "" for v in values]
            ax_.bar_label(
                container,
                labels=labels,
                label_type="center",
                fontsize=theme.value_fontsize,
                zorder=ZORDER_LABELS,
            )

        bottom += values

    if horiz:
        ax_.set_yticks(positions)
        ax_.set_yticklabels(bar_labels, fontsize=theme.tick_fontsize)
    else:
        ax_.set_xticks(positions)
        rotation, ha = tick_rotation(n_bars)
        ax_.set_xticklabels(bar_labels, fontsize=theme.tick_fontsize, rotation=rotation, ha=ha)

    set_labels(ax_, xlabel=xlabel, ylabel=ylabel, title=title)
    ax_.legend(fontsize=theme.tick_fontsize)
    setup_grid(ax_, orientation)
    finalize(fig, owns_figure=owns)
    return fig, ax_

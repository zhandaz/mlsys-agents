"""Stacked bar chart: segments stacked within each bar.

Example (horizontal repo breakdown)::

    from mlsys_agents.plot import stacked_bar, save

    data = {
        "verl": {"algo": 32, "config": 18, "distributed": 12},
        "OpenRLHF": {"algo": 15, "config": 10, "distributed": 8},
    }
    fig, ax = stacked_bar(
        data,
        orientation="horizontal",
        xlabel="Number of Silent Bugs",
        show_values=True,
        legend_kw={"loc": "upper center", "bbox_to_anchor": (0.5, 1.2), "ncol": 3},
        figsize=(10, 4),
    )
    save(fig, "repo_breakdown")
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
    setup_legend,
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
    ylim: tuple[float, float] | None = None,
    orientation: Orientation = "vertical",
    show_values: bool = False,
    value_fmt: str = ".0f",
    bar_label_fontsize: float | None = None,
    bar_label_rotation: float = 0,
    bar_label_padding: float = 2,
    show_legend: bool = True,
    legend_kw: dict[str, Any] | None = None,
    show_grid: bool = True,
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
        ylim: Y-axis limits ``(min, max)``.
        orientation: ``"vertical"`` (default) or ``"horizontal"``.
        show_values: Annotate non-zero segments with their value.
        value_fmt: Format string for value annotations.
        bar_label_fontsize: Font size for bar value labels (default from theme).
        bar_label_rotation: Rotation angle for bar value labels (default ``0``).
        bar_label_padding: Padding between bar and value label in points (default ``2``).
        show_legend: Show the legend (default ``True``). Set to ``False`` for shared legends.
        legend_kw: Extra kwargs passed to ``ax.legend()`` (e.g., ``loc``, ``ncol``, ``bbox_to_anchor``).
        show_grid: Show grid lines (default ``True``).
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
            label_fs = bar_label_fontsize if bar_label_fontsize is not None else theme.value_fontsize
            labels = [format(v, value_fmt) if v > 0 else "" for v in values]
            ax_.bar_label(
                container,
                labels=labels,
                label_type="center",
                fontsize=label_fs,
                padding=bar_label_padding,
                rotation=bar_label_rotation,
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

    set_labels(ax_, xlabel=xlabel, ylabel=ylabel, title=title, ylim=ylim)
    setup_legend(ax_, show=show_legend, legend_kw=legend_kw)
    setup_grid(ax_, orientation, show=show_grid)
    finalize(fig, owns_figure=owns)
    return fig, ax_

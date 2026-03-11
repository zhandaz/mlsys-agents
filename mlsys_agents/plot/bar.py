"""Simple bar chart: one bar per category.

Example::

    from mlsys_agents.plot import bar, save

    fig, ax = bar(
        {"algo": 78, "config": 52, "distributed": 41, "data": 28},
        sort="descending",
        ylabel="Number of Silent Bugs",
        show_values=True,
        bar_label_fontsize=9,
        figsize=(10, 4),
    )
    save(fig, "taxonomy_distribution")
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from mlsys_agents.plot.common import (
    ZORDER_BARS,
    ZORDER_LABELS,
    Orientation,
    SortOrder,
    auto_figsize,
    finalize,
    make_fig_ax,
    resolve_colors,
    resolve_display_names,
    set_labels,
    setup_grid,
    tick_rotation,
)
from mlsys_agents.plot.theme import get_theme

if TYPE_CHECKING:
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure


def bar(
    data: dict[str, float] | list[tuple[str, float]],
    *,
    ylabel: str | None = None,
    xlabel: str | None = None,
    title: str | None = None,
    ylim: tuple[float, float] | None = None,
    sort: SortOrder | None = None,
    show_values: bool = False,
    value_fmt: str = ".0f",
    bar_label_fontsize: float | None = None,
    bar_label_rotation: float = 0,
    bar_label_padding: float = 2,
    orientation: Orientation = "vertical",
    show_grid: bool = True,
    palette: str | None = None,
    colors: dict[str, str] | list[str] | None = None,
    figsize: tuple[float, float] | None = None,
    ax: Axes | None = None,
) -> tuple[Figure, Axes]:
    """Create a simple bar chart.

    Args:
        data: Mapping of category names to values. Accepts a dict or list of
            ``(name, value)`` tuples (to preserve custom ordering).
        ylabel: Y-axis label.
        xlabel: X-axis label.
        title: Figure title.
        ylim: Y-axis limits ``(min, max)``.
        sort: ``"descending"``, ``"ascending"``, or ``None`` (keep input order).
        show_values: Annotate bars with their numeric value.
        value_fmt: Format string for value annotations (default ``".0f"``).
        bar_label_fontsize: Font size for bar value labels (default from theme).
        bar_label_rotation: Rotation angle for bar value labels (default ``0``).
        bar_label_padding: Padding between bar and value label in points (default ``2``).
        orientation: ``"vertical"`` (default) or ``"horizontal"``.
        show_grid: Show grid lines (default ``True``).
        palette: Name of a registered palette for automatic color resolution.
        colors: Explicit colors (dict or list). Overrides *palette*.
        figsize: Figure size ``(width, height)`` in inches. Auto-computed if omitted.
        ax: Existing axes to draw on. If ``None``, a new figure is created.

    Returns:
        ``(Figure, Axes)`` tuple for further customization.
    """
    # Normalize input
    if isinstance(data, dict):
        items = list(data.items())
    else:
        items = list(data)

    if not items:
        msg = "No data to plot"
        raise ValueError(msg)

    if sort == "descending":
        items.sort(key=lambda x: x[1], reverse=True)
    elif sort == "ascending":
        items.sort(key=lambda x: x[1])

    keys = [k for k, _ in items]
    values = [v for _, v in items]

    theme = get_theme()
    color_list = resolve_colors(keys, palette=palette, colors=colors)
    display_names = resolve_display_names(keys, palette=palette)

    fig, ax_, owns = make_fig_ax(figsize or auto_figsize(len(keys), orientation), ax)

    horiz = orientation == "horizontal"

    if horiz:
        bars = ax_.barh(
            range(len(keys)),
            values,
            color=color_list,
            edgecolor=theme.edge_color,
            linewidth=theme.edge_width,
            zorder=ZORDER_BARS,
        )
        ax_.set_yticks(range(len(keys)))
        ax_.set_yticklabels(display_names, fontsize=theme.tick_fontsize)
    else:
        bars = ax_.bar(
            range(len(keys)),
            values,
            color=color_list,
            edgecolor=theme.edge_color,
            linewidth=theme.edge_width,
            zorder=ZORDER_BARS,
        )
        ax_.set_xticks(range(len(keys)))
        rotation, ha = tick_rotation(len(keys))
        ax_.set_xticklabels(display_names, fontsize=theme.tick_fontsize, rotation=rotation, ha=ha)

    if show_values:
        label_fs = bar_label_fontsize if bar_label_fontsize is not None else theme.value_fontsize
        labels = [format(v, value_fmt) for v in values]
        ax_.bar_label(
            bars, labels=labels, fontsize=label_fs, padding=bar_label_padding, rotation=bar_label_rotation,
            zorder=ZORDER_LABELS,
        )

    set_labels(ax_, xlabel=xlabel, ylabel=ylabel, title=title, ylim=ylim)
    setup_grid(ax_, orientation, show=show_grid)
    finalize(fig, owns_figure=owns)
    return fig, ax_

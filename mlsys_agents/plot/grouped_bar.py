"""Grouped bar chart: multiple methods compared across groups.

Example::

    from mlsys_agents.plot import grouped_bar, save

    data = {
        "A100": {"Megatron": 1.0, "DeepSpeed": 0.85},
        "H100": {"Megatron": 1.5, "DeepSpeed": 1.3},
    }
    fig, ax = grouped_bar(data, ylabel="Throughput (tok/s)", show_values=True)
    save(fig, "throughput_comparison")
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

from mlsys_agents.plot.common import (
    ZORDER_BARS,
    ZORDER_LABELS,
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
    from collections.abc import Callable

    from matplotlib.axes import Axes
    from matplotlib.figure import Figure


def grouped_bar(
    data: dict[str, dict[str, float]],
    *,
    ylabel: str | None = None,
    xlabel: str | None = None,
    title: str | None = None,
    show_values: bool = False,
    value_fmt: str = ".0f",
    bar_label_processor: Callable[[str, str, Any], str] | None = None,
    hatches: dict[str, str] | list[str] | None = None,
    palette: str | None = None,
    colors: dict[str, str] | list[str] | None = None,
    figsize: tuple[float, float] | None = None,
    ax: Axes | None = None,
) -> tuple[Figure, Axes]:
    """Create a grouped bar chart.

    Args:
        data: ``{group_label: {method: value}}``. Methods appear as adjacent bars
            within each group. All groups should have the same method keys.
        ylabel: Y-axis label.
        xlabel: X-axis label.
        title: Figure title.
        show_values: Annotate bars with their numeric value.
        value_fmt: Format string for value annotations.
        bar_label_processor: ``(group, method, value) -> str`` for custom labels.
        hatches: Hatch patterns per method (dict or list).
        palette: Name of a registered palette (resolves method keys).
        colors: Explicit colors per method. Overrides *palette*.
        figsize: Figure size in inches. Auto-computed if omitted.
        ax: Existing axes to draw on.

    Returns:
        ``(Figure, Axes)`` tuple.
    """
    if not data:
        msg = "No data to plot"
        raise ValueError(msg)

    group_labels = list(data.keys())
    methods = unique_inner_keys(data)

    n_groups = len(group_labels)
    n_methods = len(methods)

    theme = get_theme()
    color_list = resolve_colors(methods, palette=palette, colors=colors)
    method_display = resolve_display_names(methods, palette=palette)

    fig, ax_, owns = make_fig_ax(figsize or auto_figsize(n_groups * n_methods), ax)

    bar_width = 0.8 / n_methods
    x = np.arange(n_groups)

    for j, method in enumerate(methods):
        values = [data[g].get(method, 0) for g in group_labels]
        offset = (j - n_methods / 2 + 0.5) * bar_width

        bar_kw: dict[str, Any] = {
            "color": color_list[j],
            "edgecolor": theme.edge_color,
            "linewidth": theme.edge_width,
            "zorder": ZORDER_BARS,
        }
        if hatches is not None:
            if isinstance(hatches, dict):
                h = hatches.get(method)
            else:
                h = hatches[j % len(hatches)]
            if h:
                bar_kw["hatch"] = h

        container = ax_.bar(x + offset, values, bar_width, label=method_display[j], **bar_kw)

        if show_values:
            if bar_label_processor is not None:
                labels = [bar_label_processor(g, method, data[g].get(method, 0)) for g in group_labels]
            else:
                labels = [format(v, value_fmt) for v in values]
            ax_.bar_label(container, labels=labels, fontsize=theme.value_fontsize, padding=2, zorder=ZORDER_LABELS)

    ax_.set_xticks(x)
    rotation, ha = tick_rotation(n_groups)
    ax_.set_xticklabels(group_labels, fontsize=theme.tick_fontsize, rotation=rotation, ha=ha)

    set_labels(ax_, xlabel=xlabel, ylabel=ylabel, title=title)
    ax_.legend(fontsize=theme.tick_fontsize)
    setup_grid(ax_)
    finalize(fig, owns_figure=owns)
    return fig, ax_

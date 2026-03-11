"""Multi-line plot: multiple series on shared axes.

Example::

    from mlsys_agents.plot import line, save

    data = {
        "PPO": [0.5, 0.6, 0.7, 0.75, 0.78],
        "DPO": [0.4, 0.55, 0.65, 0.72, 0.76],
    }
    fig, ax = line(data, x=[1, 2, 3, 4, 5], ylabel="Reward", xlabel="Epoch")
    save(fig, "training_curves")
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from mlsys_agents.plot.common import (
    ZORDER_LINES,
    ZORDER_MARKERS,
    finalize,
    make_fig_ax,
    resolve_colors,
    resolve_display_names,
    set_labels,
    setup_grid,
)
from mlsys_agents.plot.theme import get_theme

if TYPE_CHECKING:
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure

# Default marker cycle
_MARKERS = ["o", "s", "^", "D", "v", "p", "h", "*", "X", "P"]


def line(
    data: dict[str, list[float]] | dict[str, dict[float, float]],
    *,
    x: list[float] | None = None,
    ylabel: str | None = None,
    xlabel: str | None = None,
    title: str | None = None,
    markers: bool = True,
    line_styles: dict[str, str] | list[str] | None = None,
    log_x: bool = False,
    log_y: bool = False,
    palette: str | None = None,
    colors: dict[str, str] | list[str] | None = None,
    figsize: tuple[float, float] | None = None,
    ax: Axes | None = None,
) -> tuple[Figure, Axes]:
    """Create a multi-line plot.

    Args:
        data: ``{series_name: [y_values]}`` (requires shared *x*) or
            ``{series_name: {x: y}}``.
        x: Shared x-values when data values are plain lists.
        ylabel: Y-axis label.
        xlabel: X-axis label.
        title: Figure title.
        markers: Show markers at data points (default ``True``).
        line_styles: Per-series line styles as dict or list.
        log_x: Use logarithmic x-axis.
        log_y: Use logarithmic y-axis.
        palette: Name of a registered palette.
        colors: Explicit colors per series. Overrides *palette*.
        figsize: Figure size in inches.
        ax: Existing axes to draw on.

    Returns:
        ``(Figure, Axes)`` tuple.
    """
    if not data:
        msg = "No data to plot"
        raise ValueError(msg)

    series_names = list(data.keys())
    theme = get_theme()
    color_list = resolve_colors(series_names, palette=palette, colors=colors)
    display_names = resolve_display_names(series_names, palette=palette)

    fig, ax_, owns = make_fig_ax(figsize or (8, 5), ax)

    # Pre-compute shared x once outside the loop
    shared_x = list(x) if x is not None else None

    for i, name in enumerate(series_names):
        series = data[name]

        if isinstance(series, dict):
            x_vals = list(series.keys())
            y_vals = list(series.values())
        else:
            x_vals = shared_x if shared_x is not None else list(range(len(series)))
            y_vals = list(series)

        # Resolve line style
        ls = "-"
        if line_styles is not None:
            if isinstance(line_styles, dict):
                ls = line_styles.get(name, "-")
            else:
                ls = line_styles[i % len(line_styles)]

        marker = _MARKERS[i % len(_MARKERS)] if markers else None

        ax_.plot(
            x_vals,
            y_vals,
            color=color_list[i],
            label=display_names[i],
            linestyle=ls,
            marker=marker,
            markersize=6,
            linewidth=1.5,
            zorder=ZORDER_MARKERS if markers else ZORDER_LINES,
        )

    if log_x:
        ax_.set_xscale("log")
    if log_y:
        ax_.set_yscale("log")

    set_labels(ax_, xlabel=xlabel, ylabel=ylabel, title=title)
    ax_.tick_params(labelsize=theme.tick_fontsize)
    ax_.legend(fontsize=theme.tick_fontsize)
    setup_grid(ax_)
    finalize(fig, owns_figure=owns)
    return fig, ax_

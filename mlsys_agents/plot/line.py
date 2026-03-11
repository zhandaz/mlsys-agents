"""Multi-line plot: multiple series on shared axes.

Example (kernel performance comparison)::

    from mlsys_agents.plot import line, save

    data = {
        "Megatron": {2048: 0.85, 4096: 0.92, 8192: 0.97},
        "DeepSpeed": {2048: 0.70, 4096: 0.78, 8192: 0.84},
    }
    fig, ax = line(
        data,
        ylabel="Normalized Throughput",
        xlabel="# Tokens",
        linewidth=1.5,
        markersize=4,
        xlim=(1600, 8800),
        ylim=(0.5, 1.1),
    )
    save(fig, "kernel_perf")
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from mlsys_agents.plot.common import (
    ZORDER_LINES,
    ZORDER_MARKERS,
    finalize,
    make_fig_ax,
    resolve_colors,
    resolve_display_names,
    set_labels,
    setup_grid,
    setup_legend,
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
    xlim: tuple[float, float] | None = None,
    ylim: tuple[float, float] | None = None,
    markers: bool = True,
    linewidth: float = 1.5,
    markersize: float = 6,
    line_styles: dict[str, str] | list[str] | None = None,
    log_x: bool = False,
    log_y: bool = False,
    show_legend: bool = True,
    legend_kw: dict[str, Any] | None = None,
    show_grid: bool = True,
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
        xlim: X-axis limits ``(min, max)``.
        ylim: Y-axis limits ``(min, max)``.
        markers: Show markers at data points (default ``True``).
        linewidth: Line width (default ``1.5``).
        markersize: Marker size (default ``6``).
        line_styles: Per-series line styles as dict or list.
        log_x: Use logarithmic x-axis.
        log_y: Use logarithmic y-axis.
        show_legend: Show the legend (default ``True``). Set to ``False`` for shared legends.
        legend_kw: Extra kwargs passed to ``ax.legend()`` (e.g., ``loc``, ``ncol``, ``bbox_to_anchor``).
        show_grid: Show grid lines (default ``True``).
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
            markersize=markersize,
            linewidth=linewidth,
            zorder=ZORDER_MARKERS if markers else ZORDER_LINES,
        )

    if log_x:
        ax_.set_xscale("log")
    if log_y:
        ax_.set_yscale("log")

    set_labels(ax_, xlabel=xlabel, ylabel=ylabel, title=title, xlim=xlim, ylim=ylim)
    ax_.tick_params(labelsize=theme.tick_fontsize)
    setup_legend(ax_, show=show_legend, legend_kw=legend_kw)
    setup_grid(ax_, show=show_grid)
    finalize(fig, owns_figure=owns)
    return fig, ax_

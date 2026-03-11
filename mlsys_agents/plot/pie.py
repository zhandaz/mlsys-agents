"""Pie chart: proportional slices.

Example::

    from mlsys_agents.plot import pie, save

    fig, ax = pie({"Compute": 60, "I/O": 25, "Idle": 15}, title="GPU Time Breakdown")
    save(fig, "gpu_time_pie")
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from mlsys_agents.plot.common import finalize, make_fig_ax, resolve_colors, resolve_display_names, set_labels
from mlsys_agents.plot.theme import get_theme

if TYPE_CHECKING:
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure


def pie(
    data: dict[str, float],
    *,
    title: str | None = None,
    show_pct: bool = True,
    pct_fmt: str = ".1f",
    explode: dict[str, float] | list[float] | None = None,
    palette: str | None = None,
    colors: dict[str, str] | list[str] | None = None,
    figsize: tuple[float, float] | None = None,
    ax: Axes | None = None,
) -> tuple[Figure, Axes]:
    """Create a pie chart.

    Args:
        data: ``{slice_name: value}``.
        title: Figure title.
        show_pct: Show percentage labels on slices (default ``True``).
        pct_fmt: Format string for percentage labels.
        explode: Offset for specific slices (dict keyed by name, or list).
        palette: Name of a registered palette.
        colors: Explicit colors per slice. Overrides *palette*.
        figsize: Figure size in inches.
        ax: Existing axes to draw on.

    Returns:
        ``(Figure, Axes)`` tuple.
    """
    if not data:
        msg = "No data to plot"
        raise ValueError(msg)

    keys = list(data.keys())
    values = list(data.values())
    theme = get_theme()
    color_list = resolve_colors(keys, palette=palette, colors=colors)
    display_names = resolve_display_names(keys, palette=palette)

    # Resolve explode
    explode_vals: list[float] | None = None
    if explode is not None:
        if isinstance(explode, dict):
            explode_vals = [explode.get(k, 0) for k in keys]
        else:
            explode_vals = list(explode)

    fig, ax_, owns = make_fig_ax(figsize or (6, 6), ax)

    autopct = f"%{pct_fmt}%%" if show_pct else None
    ax_.pie(
        values,
        labels=display_names,
        colors=color_list,
        autopct=autopct,
        explode=explode_vals,
        textprops={"fontsize": theme.tick_fontsize},
        wedgeprops={"edgecolor": theme.edge_color, "linewidth": theme.edge_width},
    )

    set_labels(ax_, title=title)
    finalize(fig, owns_figure=owns)
    return fig, ax_

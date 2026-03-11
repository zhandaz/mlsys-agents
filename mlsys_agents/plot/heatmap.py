"""Heatmap chart: 2D grid with color-coded cells and annotations.

Example::

    from mlsys_agents.plot import heatmap, save

    data = {
        "LoRA r=8": {"64K": 1.52, "128K": 1.41, "256K": 1.33},
        "LoRA r=16": {"64K": 1.48, "128K": 1.35, "256K": 1.28},
    }
    fig, ax = heatmap(data, ylabel="Configuration", xlabel="Sequence Length")
    save(fig, "lora_rank_seqlen")
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from mlsys_agents.plot.common import (
    finalize,
    make_fig_ax,
    resolve_display_names,
    set_labels,
    tick_rotation,
    unique_inner_keys,
)
from mlsys_agents.plot.theme import get_theme

if TYPE_CHECKING:
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure


def heatmap(
    data: dict[str, dict[str, float]] | list[list[float]],
    *,
    rows: list[str] | None = None,
    cols: list[str] | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    title: str | None = None,
    annotate: bool = True,
    annotation_fmt: str = ".0f",
    colormap: str = "YlOrRd",
    show_colorbar: bool = True,
    row_palette: str | None = None,
    col_palette: str | None = None,
    figsize: tuple[float, float] | None = None,
    ax: Axes | None = None,
) -> tuple[Figure, Axes]:
    """Create an annotated heatmap.

    Args:
        data: Nested dict ``{row_key: {col_key: value}}`` or 2D list. When using
            a 2D list, *rows* and *cols* must be provided.
        rows: Row labels (required if *data* is a 2D list).
        cols: Column labels (required if *data* is a 2D list).
        xlabel: X-axis label.
        ylabel: Y-axis label.
        title: Figure title.
        annotate: Show numeric values in each cell (default ``True``).
        annotation_fmt: Format string for cell annotations.
        colormap: Matplotlib colormap name.
        show_colorbar: Whether to display a color bar.
        row_palette: Palette name for resolving row display names.
        col_palette: Palette name for resolving column display names.
        figsize: Figure size in inches.
        ax: Existing axes to draw on.

    Returns:
        ``(Figure, Axes)`` tuple.
    """
    # Normalize to numpy array + labels
    if isinstance(data, dict):
        if not data:
            msg = "No data to plot"
            raise ValueError(msg)
        row_keys = list(data.keys())
        col_keys = unique_inner_keys(data)
        arr = np.array([[data[r].get(c, 0) for c in col_keys] for r in row_keys], dtype=float)
        rows = rows or row_keys
        cols = cols or col_keys
    else:
        if rows is None or cols is None:
            msg = "rows and cols are required when data is a 2D list"
            raise ValueError(msg)
        arr = np.array(data, dtype=float)

    theme = get_theme()
    n_rows, n_cols = arr.shape

    default_size = (max(6, n_cols * 1.2), max(4, n_rows * 0.6))
    fig, ax_, owns = make_fig_ax(figsize or default_size, ax)

    row_display = resolve_display_names(rows, palette=row_palette)
    col_display = resolve_display_names(cols, palette=col_palette)

    im = ax_.imshow(arr, cmap=colormap, aspect="auto")

    ax_.set_xticks(np.arange(n_cols))
    ax_.set_yticks(np.arange(n_rows))
    rotation, ha = tick_rotation(n_cols, threshold=4, angle=45)
    ax_.set_xticklabels(col_display, fontsize=theme.tick_fontsize, rotation=rotation, ha=ha)
    ax_.set_yticklabels(row_display, fontsize=theme.tick_fontsize)

    set_labels(ax_, xlabel=xlabel, ylabel=ylabel, title=title)

    if annotate:
        thresh = arr.max() / 2.0
        for i in range(n_rows):
            for j in range(n_cols):
                val = arr[i, j]
                if val == 0:
                    continue
                color = "white" if val > thresh else "black"
                ax_.text(
                    j,
                    i,
                    format(val, annotation_fmt),
                    ha="center",
                    va="center",
                    color=color,
                    fontsize=theme.value_fontsize,
                )

    if show_colorbar:
        fig.colorbar(im, ax=ax_, fraction=0.046, pad=0.04)

    finalize(fig, owns_figure=owns)
    return fig, ax_

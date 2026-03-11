---
name: mlsys-agents-plot
description: Generate publication-quality academic figures using mlsys_agents.plot.
user-invocable: false
---

# mlsys_agents.plot: API Reference

## Setup

```python
from mlsys_agents.plot import bar, grouped_bar, stacked_bar, heatmap, line, pie, save
from mlsys_agents.plot import Palette, set_theme
```

## Theme & Palette Registration

Register palettes once; all chart functions auto-resolve colors and display names from data keys.

```python
set_theme(palettes={
    "methods": Palette(
        colors={"lora": "#2D6A4F", "full_ft": "#264653", "qlora": "#52B788"},
        display_names={"lora": "LoRA", "full_ft": "Full Fine-Tune", "qlora": "QLoRA"},
    ),
    "phases": Palette(
        colors={"compute": "#E76F51", "io": "#F4A261", "idle": "#E9C46A"},
        display_names={"compute": "Compute", "io": "I/O", "idle": "Idle"},
    ),
})
```

Theme fields: `base_fontsize` (default 13), `dpi` (300), `formats` (["pdf", "png"]), `edge_color`, `edge_width`, `grid_alpha`. Derived: `tick_fontsize` = 85% base, `value_fontsize` = 70% base.

## Chart Functions

All return `(Figure, Axes)`. Common kwargs: `ylabel`, `xlabel`, `title`, `palette`, `colors`, `figsize`, `ax`.

### bar(): Simple Bar Chart

```python
bar(
    data: dict[str, float] | list[tuple[str, float]],
    *, ylabel=None, xlabel=None, title=None,
    ylim=None,                     # (min, max) tuple
    sort=None,                     # "descending" | "ascending" | None
    show_values=False, value_fmt=".0f",
    bar_label_fontsize=None,       # default from theme
    bar_label_rotation=0,
    bar_label_padding=2,
    orientation="vertical",        # "vertical" | "horizontal"
    show_grid=True,
    palette=None, colors=None, figsize=None, ax=None,
) -> tuple[Figure, Axes]
```

Example:
```python
fig, ax = bar({"LoRA": 1.52, "Full FT": 1.00, "QLoRA": 1.38}, ylabel="Speedup", show_values=True)
save(fig, "method_speedup")
```

### grouped_bar(): Grouped Bar Chart

```python
grouped_bar(
    data: dict[str, dict[str, float]],  # {group: {method: value}}
    *, ylabel=None, xlabel=None, title=None,
    ylim=None,
    show_values=False, value_fmt=".0f",
    bar_label_fontsize=None, bar_label_rotation=0, bar_label_padding=2,
    bar_label_processor=None,  # (group, method, value) -> str
    hatches=None,              # dict or list of hatch patterns
    show_legend=True, legend_kw=None,  # e.g. {"loc": "upper left", "ncol": 2}
    show_grid=True,
    palette=None, colors=None, figsize=None, ax=None,
) -> tuple[Figure, Axes]
```

Example:
```python
data = {
    "64K": {"Megatron": 1.0, "DeepSpeed": 0.85},
    "128K": {"Megatron": 1.5, "DeepSpeed": 1.3},
}
fig, ax = grouped_bar(data, ylabel="Throughput (tok/s)", show_values=True)
```

### stacked_bar(): Stacked Bar Chart

```python
stacked_bar(
    data: dict[str, dict[str, float]],  # {bar_label: {segment: value}}
    *, ylabel=None, xlabel=None, title=None,
    ylim=None,
    orientation="vertical",
    show_values=False, value_fmt=".0f",
    bar_label_fontsize=None, bar_label_rotation=0, bar_label_padding=2,
    show_legend=True, legend_kw=None,
    show_grid=True,
    palette=None, colors=None, figsize=None, ax=None,
) -> tuple[Figure, Axes]
```

Example:
```python
data = {
    "LLaMA-7B": {"compute": 0.6, "io": 0.25, "idle": 0.15},
    "LLaMA-13B": {"compute": 0.7, "io": 0.2, "idle": 0.1},
}
fig, ax = stacked_bar(data, ylabel="Time (normalized)", palette="phases")
```

### heatmap(): Annotated Heatmap

```python
heatmap(
    data: dict[str, dict[str, float]] | list[list[float]],
    *, rows=None, cols=None,
    xlabel=None, ylabel=None, title=None,
    annotate=True, annotation_fmt=".0f",
    colormap="YlOrRd", show_colorbar=True,
    row_palette=None, col_palette=None,
    figsize=None, ax=None,
) -> tuple[Figure, Axes]
```

Example:
```python
data = {
    "LoRA r=8": {"64K": 1.52, "128K": 1.41, "256K": 1.33},
    "LoRA r=16": {"64K": 1.48, "128K": 1.35, "256K": 1.28},
}
fig, ax = heatmap(data, ylabel="Configuration", xlabel="Sequence Length")
```

### line(): Multi-Line Plot

```python
line(
    data: dict[str, list[float]] | dict[str, dict[float, float]],
    *, x=None,  # shared x-values if data is {name: [y_values]}
    ylabel=None, xlabel=None, title=None,
    xlim=None, ylim=None,
    markers=True, linewidth=1.5, markersize=6,
    line_styles=None,
    log_x=False, log_y=False,
    show_legend=True, legend_kw=None,
    show_grid=True,
    palette=None, colors=None, figsize=None, ax=None,
) -> tuple[Figure, Axes]
```

Example:
```python
data = {"Megatron": [1.0, 1.2, 1.5], "DeepSpeed": [0.9, 1.1, 1.3]}
fig, ax = line(data, x=[64, 128, 256], ylabel="Throughput (tok/s)", xlabel="Seq Length (K)")
```

### pie(): Pie Chart

```python
pie(
    data: dict[str, float],
    *, title=None,
    show_pct=True, pct_fmt=".1f",
    explode=None,  # dict or list of offsets
    palette=None, colors=None, figsize=None, ax=None,
) -> tuple[Figure, Axes]
```

### save(): Export Helper

```python
save(fig, path, *, formats=None, close=True, dpi=None) -> list[Path]
```

Saves to PDF + PNG by default (configurable via theme). Closes figure after saving. Path should omit extension.

## Post-call Customization

All functions return `(Figure, Axes)`, so anything not covered by kwargs can be done post-call:

```python
# Shared legend across subplots
fig, axes = plt.subplots(1, 3)
_, ax1 = grouped_bar(data1, ax=axes[0], show_legend=False)
_, ax2 = grouped_bar(data2, ax=axes[1], show_legend=False)
handles, labels = ax1.get_legend_handles_labels()
fig.legend(handles, labels, loc="upper center", ncol=4)

# Y-tick formatter
from matplotlib.ticker import FuncFormatter
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x/1000)}K"))

# X-tick rotation
ax.tick_params(axis='x', rotation=45, labelsize=9)

# Custom x-ticks for line plots
ax.set_xticks([1, 2, 4, 8])
```

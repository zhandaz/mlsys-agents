# CLAUDE.md

## Project Overview

**mlsys-agents** is a monorepo of agent-native utilities for ML systems research and engineering. The first module is `mlsys_agents.plot`: a plotting library for publication-quality academic figures.

## Setup

```bash
pip install -e .
```

Dependencies: `matplotlib>=3.9`, `numpy>=1.26`.

## Architecture

### `mlsys_agents.plot` — Functional Plotting API

Every chart type is a single function that returns `(Figure, Axes)`:

- `bar()` — simple bar chart (one bar per category)
- `grouped_bar()` — adjacent bars comparing methods across groups
- `stacked_bar()` — segments stacked within each bar
- `heatmap()` — 2D grid with color-coded cells
- `line()` — multi-line plot
- `pie()` — pie chart

All functions accept `palette=` (string name) or `colors=` (explicit dict/list) for color control, and return `(Figure, Axes)` for downstream customization.

### Theme Singleton

`set_theme()` configures the global theme (font sizes, DPI, palettes). Chart functions auto-resolve from this singleton.

- `Palette(colors={key: hex}, display_names={key: label})` — maps data keys to colors and labels
- `set_theme(palettes={"name": palette}, base_fontsize=13)` — register palettes, set font scale
- `get_theme()` / `reset_theme()` — access or reset the singleton

Font size derivation: tick labels = 85% of base, value annotations = 70% of base.

### Color Resolution Order

1. Explicit `colors=` kwarg (dict or list)
2. Registered palette via `palette="name"` kwarg
3. `QUALITATIVE_10` fallback sequence

### `save(fig, path)` Helper

Saves to PDF + PNG by default, closes the figure. Returns list of saved paths.

## Testing

```bash
pip install -e ".[dev]"
pytest
```

72 tests covering all 6 chart types, theme system, save utility, and color resolution.

## Coding Conventions

- Python 3.12+ type hints (`list[str]` not `List[str]`, `X | None` not `Optional[X]`)
- Line length: 120
- Docstring convention: Google style
- Lint: `ruff` with `select = ["ALL"]` (see pyproject.toml for ignores)
- Format: `black` (line-length 120)
- Run `pre-commit run -a` before committing

## Adding a New Chart Type

1. Create `mlsys_agents/plot/<chart_type>.py` with a single public function
2. Function signature: `def chart_type(data, *, ylabel=None, ..., palette=None, colors=None, figsize=None, ax=None) -> tuple[Figure, Axes]`
3. Use `make_fig_ax()`, `resolve_colors()`, `resolve_display_names()`, `setup_grid()` from `common.py`
4. Re-export from `mlsys_agents/plot/__init__.py`

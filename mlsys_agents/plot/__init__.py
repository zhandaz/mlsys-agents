"""Publication-quality academic figures in ~3 lines of code.

Quick start::

    from mlsys_agents.plot import bar, save, Palette, set_theme

    # Optional: register a palette for automatic color/label resolution
    set_theme(palettes={"methods": Palette(
        colors={"lora": "#2D6A4F", "full_ft": "#264653"},
        display_names={"lora": "LoRA", "full_ft": "Full Fine-Tune"},
    )})

    fig, ax = bar({"lora": 1.52, "full_ft": 1.00}, ylabel="Speedup", palette="methods")
    save(fig, "my_chart")  # -> my_chart.pdf + my_chart.png
"""

from mlsys_agents.plot.bar import bar
from mlsys_agents.plot.common import auto_figsize, save
from mlsys_agents.plot.grouped_bar import grouped_bar
from mlsys_agents.plot.heatmap import heatmap
from mlsys_agents.plot.line import line
from mlsys_agents.plot.pie import pie
from mlsys_agents.plot.stacked_bar import stacked_bar
from mlsys_agents.plot.theme import Palette, Theme, get_theme, reset_theme, set_theme

__all__ = [
    "Palette",
    "Theme",
    "auto_figsize",
    "bar",
    "get_theme",
    "grouped_bar",
    "heatmap",
    "line",
    "pie",
    "reset_theme",
    "save",
    "set_theme",
    "stacked_bar",
]

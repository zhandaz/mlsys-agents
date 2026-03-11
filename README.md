# mlsys-agents

Agent-native utilities for ML systems research and engineering.

## Install

```bash
pip install -e .
```

## `mlsys_agents.plot`: Academic Figures in 3 Lines

```python
from mlsys_agents.plot import bar, save

fig, ax = bar({"LoRA": 1.52, "Full FT": 1.00, "QLoRA": 1.38}, ylabel="Speedup", show_values=True)
save(fig, "method_speedup")  # -> .pdf + .png
```

### Palette Registration

```python
from mlsys_agents.plot import Palette, set_theme

set_theme(palettes={"methods": Palette(
    colors={"lora": "#2D6A4F", "full_ft": "#264653", "qlora": "#52B788"},
    display_names={"lora": "LoRA", "full_ft": "Full Fine-Tune", "qlora": "QLoRA"},
)})
```

### Chart Types

| Function | Description |
|---|---|
| `bar(data)` | Simple bar chart |
| `grouped_bar(data)` | Methods compared across groups |
| `stacked_bar(data)` | Segments stacked within bars |
| `heatmap(data)` | 2D grid with annotations |
| `line(data)` | Multi-line plot |
| `pie(data)` | Pie chart |

All return `(Figure, Axes)`. Use `save(fig, path)` to export (PDF + PNG, auto-closes).

## Claude Code Skill

This repo ships with a [Claude Code](https://claude.ai/claude-code) skill at `.claude/skills/plot/SKILL.md`. The skill gives Claude the full `mlsys_agents.plot` API reference so it can generate figures for you.

**Using in this repo:** The skill is auto-loaded when you run Claude Code from this directory.

**Using in another project:** Copy or symlink the skill into your project's `.claude/skills/` directory:

```bash
# Option 1: symlink (stays in sync with upstream)
mkdir -p .claude/skills
ln -s /path/to/mlsys-agents/.claude/skills/plot .claude/skills/mlsys-agents-plot

# Option 2: copy
mkdir -p .claude/skills/mlsys-agents-plot
cp /path/to/mlsys-agents/.claude/skills/plot/SKILL.md .claude/skills/mlsys-agents-plot/
```

Then Claude Code will automatically use the API reference when generating plots in your project.

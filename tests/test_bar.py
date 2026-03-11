"""Tests for bar chart.

bar() is the simplest chart and doubles as the integration test surface for shared
behaviors (palette, colors, figsize, ax reuse, save). Each test exercises a realistic
combination of kwargs rather than testing individual parameters in isolation.
"""

import matplotlib.pyplot as plt
import pytest

from mlsys_agents.plot import bar, save


class TestBar:
    def test_empty_raises(self):
        with pytest.raises(ValueError, match="No data"):
            bar({})

    def test_taxonomy_distribution(self, tmp_output):
        """Reproduce a taxonomy distribution bar chart (issue_analysis style)."""
        data = {
            "algo": 78, "config": 52, "distributed": 41,
            "data": 28, "infra": 18, "numeric": 11,
        }
        fig, ax = bar(
            data,
            sort="descending",
            ylabel="Number of Silent Bugs",
            show_values=True,
            bar_label_fontsize=9,
            colors=["#264653", "#2A9D8F", "#E9C46A", "#F4A261", "#E76F51", "#1B4332"],
            figsize=(10, 4),
        )
        # Verify sort order and value labels
        labels = [t.get_text() for t in ax.get_xticklabels()]
        assert labels[0] == "algo"
        assert len(ax.texts) == 6
        paths = save(fig, tmp_output / "taxonomy_dist")
        assert len(paths) == 2
        assert all(p.exists() for p in paths)

    def test_horizontal_with_palette(self, methods_palette):
        """Test horizontal bar with palette-resolved display names."""
        fig, ax = bar(
            {"lora": 1.52, "full_ft": 1.00, "qlora": 1.38},
            orientation="horizontal",
            ylabel="Method",
            xlabel="Speedup",
            palette=methods_palette,
            show_values=True,
            value_fmt=".2f",
        )
        y_labels = [t.get_text() for t in ax.get_yticklabels()]
        assert "LoRA" in y_labels
        assert "Full Fine-Tune" in y_labels
        plt.close(fig)

    def test_existing_axes(self):
        """Verify ax= reuse returns the same figure and axes."""
        fig, ax = plt.subplots()
        fig2, ax2 = bar({"A100": 312, "H100": 489}, ax=ax)
        assert fig2 is fig
        assert ax2 is ax
        plt.close(fig)

    def test_list_input_preserves_order(self):
        """List-of-tuples input should preserve custom ordering."""
        fig, ax = bar([("Z", 1), ("A", 3), ("M", 2)])
        labels = [t.get_text() for t in ax.get_xticklabels()]
        assert labels == ["Z", "A", "M"]
        plt.close(fig)

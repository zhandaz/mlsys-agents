"""Tests for stacked bar chart."""

import matplotlib.pyplot as plt
import pytest

from mlsys_agents.plot import save, stacked_bar


class TestStackedBar:
    def test_empty_raises(self):
        with pytest.raises(ValueError, match="No data"):
            stacked_bar({})

    def test_horizontal_repo_breakdown(self, tmp_output):
        """Reproduce an issue_analysis-style horizontal repo breakdown chart.

        Horizontal stacked bar with custom legend position and no grid.
        """
        data = {
            "verl": {"algo": 32, "config": 18, "distributed": 12, "data": 8},
            "OpenRLHF": {"algo": 15, "config": 10, "distributed": 8, "data": 5},
            "NeMo-RL": {"algo": 12, "config": 8, "distributed": 6, "data": 4},
            "trl": {"algo": 10, "config": 6, "distributed": 4, "data": 2},
        }
        fig, ax = stacked_bar(
            data,
            orientation="horizontal",
            xlabel="Number of Silent Bugs",
            show_values=True,
            bar_label_fontsize=9,
            show_legend=True,
            legend_kw={
                "loc": "upper center",
                "bbox_to_anchor": (0.5, 1.2),
                "ncol": 4,
                "frameon": False,
            },
            figsize=(10, 4),
        )
        y_labels = [t.get_text() for t in ax.get_yticklabels()]
        assert "verl" in y_labels
        assert ax.get_legend() is not None

        paths = save(fig, tmp_output / "stacked_bar_e2e")
        assert all(p.exists() for p in paths)

    def test_missing_segment(self):
        """Groups with uneven segment sets should not crash."""
        data = {"A100": {"compute": 60, "io": 25}, "H100": {"compute": 70}}
        fig, ax = stacked_bar(data)
        assert fig is not None
        plt.close(fig)

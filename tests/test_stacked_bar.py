"""Tests for stacked bar chart (features unique to stacked_bar)."""

import matplotlib.pyplot as plt
import pytest

from mlsys_agents.plot import stacked_bar


class TestStackedBar:
    def test_basic_vertical(self):
        data = {"LLaMA-7B": {"compute": 0.6, "io": 0.25}, "LLaMA-13B": {"compute": 0.7, "io": 0.2}}
        fig, ax = stacked_bar(data, ylabel="Time (normalized)")
        assert fig is not None
        plt.close(fig)

    def test_horizontal(self):
        data = {"LLaMA-7B": {"compute": 0.6, "io": 0.25}, "LLaMA-13B": {"compute": 0.7, "io": 0.2}}
        fig, ax = stacked_bar(data, orientation="horizontal")
        labels = [t.get_text() for t in ax.get_yticklabels()]
        assert "LLaMA-7B" in labels
        plt.close(fig)

    def test_empty_raises(self):
        with pytest.raises(ValueError, match="No data"):
            stacked_bar({})

    def test_show_values(self):
        data = {"Model A": {"compute": 60, "io": 25}}
        fig, ax = stacked_bar(data, show_values=True)
        assert len(ax.texts) >= 2
        plt.close(fig)

    def test_legend_has_segments(self):
        data = {"Model A": {"compute": 60, "io": 25}}
        fig, ax = stacked_bar(data)
        legend_texts = [t.get_text() for t in ax.get_legend().get_texts()]
        assert "compute" in legend_texts
        assert "io" in legend_texts
        plt.close(fig)

    def test_missing_segment(self):
        data = {"A100": {"compute": 60, "io": 25}, "H100": {"compute": 70}}
        fig, ax = stacked_bar(data)
        assert fig is not None
        plt.close(fig)

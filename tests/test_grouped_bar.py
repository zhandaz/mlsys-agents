"""Tests for grouped bar chart (features unique to grouped_bar)."""

import matplotlib.pyplot as plt
import pytest

from mlsys_agents.plot import grouped_bar


class TestGroupedBar:
    def test_basic(self):
        data = {"64K": {"Megatron": 1.0, "DeepSpeed": 0.85}, "128K": {"Megatron": 1.5, "DeepSpeed": 1.3}}
        fig, ax = grouped_bar(data, ylabel="Throughput (tok/s)")
        assert fig is not None
        plt.close(fig)

    def test_empty_raises(self):
        with pytest.raises(ValueError, match="No data"):
            grouped_bar({})

    def test_show_values(self):
        data = {"A100": {"LoRA": 1.52, "Full FT": 1.00}}
        fig, ax = grouped_bar(data, show_values=True)
        assert len(ax.texts) >= 2
        plt.close(fig)

    def test_methods_in_legend(self):
        data = {"A100": {"Megatron": 1.0, "DeepSpeed": 0.85}}
        fig, ax = grouped_bar(data)
        legend_texts = [t.get_text() for t in ax.get_legend().get_texts()]
        assert "Megatron" in legend_texts
        assert "DeepSpeed" in legend_texts
        plt.close(fig)

    def test_hatches(self):
        data = {"A100": {"LoRA": 1.52, "Full FT": 1.00}}
        fig, _ = grouped_bar(data, hatches={"LoRA": "//", "Full FT": ".."})
        plt.close(fig)
        fig, _ = grouped_bar(data, hatches=["//", ".."])
        plt.close(fig)

    def test_bar_label_processor(self):
        data = {"A100": {"LoRA": 1.00, "QLoRA": 0.85}}
        fig, ax = grouped_bar(data, show_values=True, bar_label_processor=lambda _g, _m, v: f"{v:.2f}x")
        values = [t.get_text() for t in ax.texts]
        assert "1.00x" in values
        assert "0.85x" in values
        plt.close(fig)

    def test_missing_method_in_group(self):
        data = {"A100": {"LoRA": 1.52, "Full FT": 1.00}, "H100": {"LoRA": 2.10}}
        fig, ax = grouped_bar(data)
        assert fig is not None
        plt.close(fig)

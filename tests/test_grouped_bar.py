"""Tests for grouped bar chart."""

import matplotlib.pyplot as plt
import pytest

from mlsys_agents.plot import grouped_bar, save


class TestGroupedBar:
    def test_empty_raises(self):
        with pytest.raises(ValueError, match="No data"):
            grouped_bar({})

    def test_multi_panel_shared_legend(self, tmp_output):
        """Reproduce a LoRAFusion-style multi-panel figure with shared legend.

        Each panel uses show_legend=False, rotated bar labels, ylim, and hatches.
        A shared legend is added to the figure after rendering.
        """
        data_a100 = {
            "64K": {"Megatron": 4800, "DeepSpeed": 3200, "FSDP": 2900},
            "128K": {"Megatron": 3600, "DeepSpeed": 2600, "FSDP": 2400},
        }
        data_h100 = {
            "64K": {"Megatron": 7200, "DeepSpeed": 5100, "FSDP": 4500},
            "128K": {"Megatron": 5800, "DeepSpeed": 4200, "FSDP": 3800},
        }

        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        common_kw = {
            "ylabel": "Throughput (tok/s)",
            "show_values": True,
            "bar_label_fontsize": 9,
            "bar_label_rotation": 90,
            "ylim": (0, 10000),
            "show_legend": False,
            "hatches": ["", "//", ".."],
        }
        _, ax1 = grouped_bar(data_a100, ax=axes[0], title="A100", **common_kw)
        _, ax2 = grouped_bar(data_h100, ax=axes[1], title="H100", **common_kw)

        # Shared legend from first panel
        handles, labels = ax1.get_legend_handles_labels()
        fig.legend(handles, labels, loc="upper center", ncol=3, frameon=False)

        assert ax1.get_ylim() == (0, 10000)
        assert ax1.get_legend() is None  # Per-panel legend disabled
        assert len(labels) == 3

        paths = save(fig, tmp_output / "grouped_bar_e2e")
        assert all(p.exists() for p in paths)

    def test_bar_label_processor(self):
        """Custom label formatting via bar_label_processor."""
        data = {"A100": {"LoRA": 1.00, "QLoRA": 0.85}}
        fig, ax = grouped_bar(
            data,
            show_values=True,
            bar_label_processor=lambda _g, _m, v: f"{v:.2f}x",
        )
        values = [t.get_text() for t in ax.texts]
        assert "1.00x" in values
        assert "0.85x" in values
        plt.close(fig)

    def test_missing_method_in_group(self):
        """Groups with uneven method sets should not crash."""
        data = {"A100": {"LoRA": 1.52, "Full FT": 1.00}, "H100": {"LoRA": 2.10}}
        fig, ax = grouped_bar(data)
        assert fig is not None
        plt.close(fig)

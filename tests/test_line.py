"""Tests for line chart."""

import matplotlib.pyplot as plt
import pytest

from mlsys_agents.plot import line, save


class TestLine:
    def test_empty_raises(self):
        with pytest.raises(ValueError, match="No data"):
            line({})

    def test_kernel_perf_multi_panel(self, tmp_output):
        """Reproduce a LoRAFusion-style kernel performance line chart.

        Multiple series with custom linewidth, markersize, xlim, ylim,
        show_legend=False per panel, then shared legend added to figure.
        """
        data = {
            "Megatron": {2048: 0.85, 4096: 0.92, 6144: 0.95, 8192: 0.97},
            "DeepSpeed": {2048: 0.70, 4096: 0.78, 6144: 0.82, 8192: 0.84},
            "FSDP": {2048: 0.65, 4096: 0.72, 6144: 0.75, 8192: 0.77},
        }

        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        common_kw = {
            "ylabel": "Normalized Throughput",
            "xlabel": "# Tokens",
            "linewidth": 1.5,
            "markersize": 4,
            "xlim": (1600, 8800),
            "ylim": (0.5, 1.1),
            "show_legend": False,
            "show_grid": True,
        }
        _, ax1 = line(data, ax=axes[0], title="Forward", **common_kw)
        _, ax2 = line(data, ax=axes[1], title="Backward", **common_kw)

        # Shared legend
        handles, labels = ax1.get_legend_handles_labels()
        fig.legend(handles, labels, loc="upper center", ncol=3)

        assert ax1.get_xlim() == (1600, 8800)
        assert ax1.get_ylim() == (0.5, 1.1)
        assert ax1.get_lines()[0].get_linewidth() == 1.5
        assert ax1.get_lines()[0].get_markersize() == 4
        assert ax1.get_legend() is None

        paths = save(fig, tmp_output / "line_e2e")
        assert all(p.exists() for p in paths)

    def test_dict_of_dicts_input(self):
        """Dict-of-dicts input: each series is {x: y}."""
        data = {"LoRA": {64: 1.2, 128: 1.4}, "Full FT": {64: 1.0, 128: 1.1}}
        fig, ax = line(data)
        assert len(ax.get_lines()) == 2
        plt.close(fig)

    def test_log_scales(self):
        """Log-scale axes for kernel benchmarks."""
        fig, ax = line(
            {"Kernel A": [1, 10, 100]},
            x=[1, 10, 100],
            log_x=True,
            log_y=True,
        )
        assert ax.get_xscale() == "log"
        assert ax.get_yscale() == "log"
        plt.close(fig)

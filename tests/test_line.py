"""Tests for line chart (features unique to line)."""

import matplotlib.pyplot as plt
import pytest

from mlsys_agents.plot import line


class TestLine:
    def test_basic_with_shared_x(self):
        data = {"LoRA": [1.2, 1.4, 1.5], "Full FT": [1.0, 1.1, 1.15]}
        fig, ax = line(data, x=[64, 128, 256])
        assert len(ax.get_lines()) == 2
        plt.close(fig)

    def test_auto_x(self):
        fig, ax = line({"LoRA": [1.2, 1.4, 1.5]})
        assert list(ax.get_lines()[0].get_xdata()) == [0, 1, 2]
        plt.close(fig)

    def test_dict_of_dicts_input(self):
        data = {"LoRA": {64: 1.2, 128: 1.4}, "Full FT": {64: 1.0, 128: 1.1}}
        fig, ax = line(data)
        assert len(ax.get_lines()) == 2
        plt.close(fig)

    def test_empty_raises(self):
        with pytest.raises(ValueError, match="No data"):
            line({})

    def test_no_markers(self):
        fig, ax = line({"LoRA": [1.2, 1.4, 1.5]}, markers=False)
        marker = ax.get_lines()[0].get_marker()
        assert marker == "None" or marker is None
        plt.close(fig)

    def test_log_scales(self):
        fig, ax = line({"Kernel A": [1, 10, 100]}, x=[1, 10, 100], log_x=True, log_y=True)
        assert ax.get_xscale() == "log"
        assert ax.get_yscale() == "log"
        plt.close(fig)

    def test_line_styles(self):
        data = {"LoRA": [1.2, 1.4], "Full FT": [1.0, 1.1]}
        fig, _ = line(data, line_styles={"LoRA": "--", "Full FT": ":"})
        plt.close(fig)
        fig, _ = line(data, line_styles=["--", ":"])
        plt.close(fig)

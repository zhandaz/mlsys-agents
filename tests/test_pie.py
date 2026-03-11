"""Tests for pie chart (features unique to pie)."""

import matplotlib.pyplot as plt
import pytest

from mlsys_agents.plot import pie


class TestPie:
    def test_basic(self):
        fig, ax = pie({"Compute": 60, "I/O": 25, "Idle": 15})
        assert fig is not None
        plt.close(fig)

    def test_empty_raises(self):
        with pytest.raises(ValueError, match="No data"):
            pie({})

    def test_no_pct(self):
        fig, ax = pie({"Compute": 60, "I/O": 25}, show_pct=False)
        assert fig is not None
        plt.close(fig)

    def test_explode(self):
        fig, _ = pie({"Compute": 60, "I/O": 25}, explode={"Compute": 0.1})
        plt.close(fig)
        fig, _ = pie({"Compute": 60, "I/O": 25}, explode=[0.1, 0])
        plt.close(fig)

    def test_title(self):
        fig, ax = pie({"Compute": 60}, title="GPU Time Breakdown")
        assert ax.get_title() == "GPU Time Breakdown"
        plt.close(fig)

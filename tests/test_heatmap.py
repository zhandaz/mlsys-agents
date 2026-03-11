"""Tests for heatmap chart (features unique to heatmap)."""

import matplotlib.pyplot as plt
import pytest

from mlsys_agents.plot import heatmap


class TestHeatmap:
    def test_basic_dict(self):
        data = {"r=8": {"64K": 1.52, "128K": 1.41}, "r=16": {"64K": 1.48, "128K": 1.35}}
        fig, ax = heatmap(data)
        assert fig is not None
        plt.close(fig)

    def test_2d_list_input(self):
        fig, ax = heatmap([[1.52, 1.41], [1.48, 1.35]], rows=["r=8", "r=16"], cols=["64K", "128K"])
        assert fig is not None
        plt.close(fig)

    def test_2d_list_missing_labels_raises(self):
        with pytest.raises(ValueError, match="rows and cols are required"):
            heatmap([[1, 2], [3, 4]])

    def test_empty_raises(self):
        with pytest.raises(ValueError, match="No data"):
            heatmap({})

    def test_annotations_skip_zeros(self):
        data = {"r=8": {"64K": 1.52, "128K": 0}}
        fig, ax = heatmap(data, annotate=True)
        texts = [t.get_text() for t in ax.texts]
        assert len(texts) == 1  # only non-zero cell annotated
        assert "0" not in texts
        plt.close(fig)

    def test_no_annotations(self):
        data = {"r=8": {"64K": 1.52, "128K": 1.41}}
        fig, ax = heatmap(data, annotate=False)
        assert len(ax.texts) == 0
        plt.close(fig)

    def test_missing_col_in_row(self):
        data = {"r=8": {"64K": 1.52, "128K": 1.41}, "r=16": {"64K": 1.48}}
        fig, ax = heatmap(data)
        assert fig is not None
        plt.close(fig)

"""Tests for bar chart.

bar() is the simplest chart and is used as the integration test surface for shared
behaviors (labels, palette, colors, figsize, ax reuse). Other chart test files only
test features unique to their chart type.
"""

import matplotlib.pyplot as plt
import pytest

from mlsys_agents.plot import bar, save


class TestBar:
    def test_basic_dict(self):
        fig, ax = bar({"A100": 312, "H100": 489, "B200": 620})
        assert fig is not None
        assert ax is not None
        plt.close(fig)

    def test_basic_list_input(self):
        fig, ax = bar([("LoRA", 1.52), ("Full FT", 1.00)])
        assert fig is not None
        plt.close(fig)

    def test_empty_raises(self):
        with pytest.raises(ValueError, match="No data"):
            bar({})

    def test_sort(self):
        fig, ax = bar({"A100": 312, "H100": 489, "B200": 620}, sort="descending")
        labels = [t.get_text() for t in ax.get_xticklabels()]
        assert labels[0] == "B200"
        plt.close(fig)

        fig, ax = bar({"A100": 312, "H100": 489, "B200": 620}, sort="ascending")
        labels = [t.get_text() for t in ax.get_xticklabels()]
        assert labels[0] == "A100"
        plt.close(fig)

    def test_show_values(self):
        fig, ax = bar({"A100": 312, "H100": 489}, show_values=True)
        assert len(ax.texts) >= 2
        plt.close(fig)

    def test_horizontal(self):
        fig, ax = bar({"A100": 312, "H100": 489}, orientation="horizontal")
        labels = [t.get_text() for t in ax.get_yticklabels()]
        assert "A100" in labels
        plt.close(fig)

    def test_auto_rotate_many_categories(self):
        data = {f"layer_{i}": i * 10 for i in range(10)}
        fig, ax = bar(data)
        for label in ax.get_xticklabels():
            assert label.get_rotation() == 30
        plt.close(fig)

    # -- Shared behavior integration tests (tested here once for the whole library) --

    def test_labels_and_title(self):
        fig, ax = bar({"A100": 312}, ylabel="Throughput", xlabel="GPU", title="Perf")
        assert ax.get_ylabel() == "Throughput"
        assert ax.get_xlabel() == "GPU"
        assert ax.get_title() == "Perf"
        plt.close(fig)

    def test_palette_resolution(self, methods_palette):
        fig, ax = bar({"lora": 1.52, "full_ft": 1.00}, palette=methods_palette)
        labels = [t.get_text() for t in ax.get_xticklabels()]
        assert "LoRA" in labels
        assert "Full Fine-Tune" in labels
        plt.close(fig)

    def test_explicit_colors(self):
        fig, _ = bar({"A100": 312, "H100": 489}, colors={"A100": "#FF0000", "H100": "#00FF00"})
        plt.close(fig)
        fig, _ = bar({"A100": 312, "H100": 489}, colors=["#FF0000", "#00FF00"])
        plt.close(fig)

    def test_custom_figsize(self):
        fig, ax = bar({"A100": 312}, figsize=(12, 6))
        w, h = fig.get_size_inches()
        assert abs(w - 12) < 0.1
        assert abs(h - 6) < 0.1
        plt.close(fig)

    def test_existing_axes(self):
        fig, ax = plt.subplots()
        fig2, ax2 = bar({"A100": 312, "H100": 489}, ax=ax)
        assert fig2 is fig
        assert ax2 is ax
        plt.close(fig)

    def test_save_integration(self, tmp_output):
        fig, ax = bar({"A100": 312, "H100": 489})
        paths = save(fig, tmp_output / "bar_test")
        assert len(paths) == 2
        assert all(p.exists() for p in paths)

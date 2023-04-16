from typing import Any

import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns


def set_style() -> None:
    sns.set_style("whitegrid")
    mpl_config = {
        # LINES
        "lines.linewidth": 1.0,
        # BOXPLOT
        "boxplot.whiskers": 1.0,
        # AXES
        "axes.spines.left": False,
        "axes.spines.right": False,
        "axes.spines.bottom": False,
        "axes.spines.top": False,
        # TICKS
        "xtick.bottom": False,
        "ytick.left": False,
        # GRID
        "grid.linewidth": 0.5,
        # LEGEND
        "legend.frameon": False,
        "legend.handlelength": 1.0,
        "legend.columnspacing": 1.0,
        # FIGURE
        "figure.dpi": 300,
        # SAVING
        "savefig.dpi": 300,
    }
    for k, v in mpl_config.items():
        mpl.rcParams[k] = v


def move_legend(ax: plt.Axes, as_sns: bool = False, **kwargs: Any) -> None:
    ax_kwargs = {
        "alignment": "left",
        "loc": "center left",
        "bbox_to_anchor": (1, 0.5),
        **kwargs,
    }
    if as_sns:
        sns.move_legend(ax, **ax_kwargs)
    else:
        ax.legend(**ax_kwargs)

"""Generate visualizations and table outputs."""

import matplotlib.pyplot as plt
import numpy as np
import polars as pl
import seaborn as sns

from .paths import data_dir, outputs_dir, processed_historical_data
from .plot_collection import PlotCollection
from .plotting import move_legend

plots = PlotCollection()


def collect_all_data() -> pl.DataFrame:
    """Collect all of the data."""
    data_frames: list[pl.DataFrame] = [pl.read_parquet(processed_historical_data())]
    dtypes = {"date": pl.Date, "paid": bool, "amount": pl.Float32}
    for file in data_dir().iterdir():
        if file.suffix == ".csv":
            data_frames.append(pl.read_csv(file, dtypes=dtypes))
    return pl.concat(data_frames)


@plots.add
def plot_income(budget_df: pl.DataFrame) -> None:
    plot_df = (
        budget_df.filter(pl.col("type") == "Income")
        .sort("date")
        .groupby_dynamic("date", every="1mo")
        .agg(pl.col("amount").sum())
        .with_columns(
            pl.col("date").dt.month().alias("month"),
            pl.col("date").dt.year().alias("year"),
        )
        .to_pandas()
    )
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.scatterplot(plot_df, x="month", y="amount", hue="year", palette="flare", ax=ax)
    sns.lineplot(
        plot_df,
        x="month",
        y="amount",
        hue="year",
        alpha=0.5,
        palette="flare",
        legend=False,
        ax=ax,
    )
    ax.yaxis.set_major_formatter("${x:1.2f}")
    ax.set_xticks(np.arange(1, 13, 1))
    ax.set_ylabel("income")
    ax.set_xlabel("month")
    move_legend(ax, title="year")
    fig.tight_layout()
    fig.savefig(str(outputs_dir() / "income.png"), dpi=300)


def generate_report() -> None:
    data = collect_all_data()
    # print(data.head())
    plots.plot(data)

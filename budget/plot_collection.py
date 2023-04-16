"""Plot collection manager."""


from typing import Callable

import polars as pl

PlottingFunction = Callable[[pl.DataFrame], None]


class PlotCollection:
    """Plot collector."""

    def __init__(self) -> None:
        self.plotting_functions: list[PlottingFunction] = []

    def add(self, fxn: PlottingFunction) -> None:
        """Add a plotting function."""
        self.plotting_functions.append(fxn)

    def plot(self, df: pl.DataFrame) -> None:
        """Execute the plotting functions."""
        for fxn in self.plotting_functions:
            fxn(df)

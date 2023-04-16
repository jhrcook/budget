from typing import TypeVar

import polars as pl

T = TypeVar("T")


def pipe_print(df: T) -> T:
    """Print an object within a pipeline."""
    print(df)
    return df

"""Processing the data exported from Numbers."""

from pathlib import Path

import polars as pl
from loguru import logger


def _parse_date_col(lazyf: pl.LazyFrame) -> pl.LazyFrame:
    return lazyf.with_columns(pl.col("date").str.strptime(pl.Date, fmt="%m/%d/%y"))


def _set_column_order(lazyf: pl.LazyFrame) -> pl.LazyFrame:
    return lazyf.select(["date", "amount", "type", "name", "payment_method", "paid"])


def _parse_currency(lazyf: pl.LazyFrame) -> pl.LazyFrame:
    return lazyf.with_columns(pl.col("amount").str.replace("\\$", "").cast(pl.Float32))


def _process_expenses(df_path: Path) -> pl.LazyFrame:
    df = pl.scan_csv(df_path).rename(
        {
            "Date": "date",
            "Amount": "amount",
            "Type": "type",
            "Expense": "name",
            "Payment Method": "payment_method",
        }
    )
    if "Credit Paid" not in df.columns:
        df = df.with_columns(paid=pl.lit(True))
    else:
        df = df.rename({"Credit Paid": "paid"}).with_columns(
            pl.col("paid").cast(pl.Boolean)
        )

    return df.pipe(_parse_date_col).pipe(_set_column_order).pipe(_parse_currency)


def _process_income(df_path: Path) -> pl.LazyFrame:
    df = (
        pl.scan_csv(df_path)
        .rename({"Amount": "amount", "Date": "date", "Source": "name"})
        .with_columns(
            paid=pl.lit(True),
            payment_method=pl.lit("direct deposit"),
            type=pl.lit("Income"),
        )
        .pipe(_parse_date_col)
        .pipe(_parse_currency)
        .pipe(_set_column_order)
    )
    return df


def process_old_data_export(dir: Path, output: Path) -> None:
    data_frames: list[pl.LazyFrame] = []
    for file in dir.iterdir():
        if "Taxes" in file.name:
            continue
        elif file.name.endswith("Expenses.csv"):
            logger.debug(f"New expenses file: {file.name}")
            expenses = _process_expenses(file)
            data_frames.append(expenses)
        elif file.name.endswith("Income.csv"):
            logger.debug(f"New income file: {file.name}")
            income = _process_income(file)
            data_frames.append(income)
    pl.concat(data_frames).collect().write_parquet(output)

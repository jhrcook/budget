"""Project paths."""

from pathlib import Path


def data_dir() -> Path:
    d = Path("data")
    if not d.exists():
        d.mkdir()
    return d


def historical_data_dir() -> Path:
    return Path("historical-data")


def processed_historical_data() -> Path:
    return data_dir() / "historical-data.parquet"

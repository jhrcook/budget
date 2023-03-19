"""Command line interface."""

from loguru import logger
import typer

from .exported_data import process_old_data_export
from .paths import historical_data_dir, processed_historical_data

app = typer.Typer()


@app.command()
def process_historical_data() -> None:
    logger.info("Processing historical data.")
    process_old_data_export(historical_data_dir(), output=processed_historical_data())


@app.command()
def process_data() -> None:
    ...


@app.command()
def new_sheet() -> None:
    print("new month program boop bop beep")


@app.command()
def generate_reports() -> None:
    print("generate reports beep beep boop")

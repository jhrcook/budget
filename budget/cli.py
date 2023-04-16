"""Command line interface."""

import typer
from loguru import logger

from .budget_data import new_from_user_input, this_months_sheet
from .historical_data import process_old_data_export
from .paths import historical_data_dir, processed_historical_data
from .plotting import set_style
from .report import generate_report

app = typer.Typer(
    help="Budget data collection and analysis app.",
    epilog="Developed with :heart: by Josh Cook.",
    add_completion=False,
    pretty_exceptions_enable=False,
)


@app.command()
def process_historical_data() -> None:
    logger.info("Processing historical data.")
    process_old_data_export(historical_data_dir(), output=processed_historical_data())


@app.command()
def process_data() -> None:
    ...


app.command(name="add")(new_from_user_input)


@app.command()
def new_sheet() -> None:
    sheet_name = this_months_sheet()
    logger.info(f"current sheet: {sheet_name}")


@app.command(name="report")
def report() -> None:
    set_style()
    generate_report()

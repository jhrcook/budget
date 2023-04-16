"""Nox commands."""

import nox

nox.options.reuse_existing_virtualenvs = True


@nox.session()
def black(session: nox.Session) -> None:
    """Black formatter."""
    session.install("black")
    session.run("black", "budget/")
    session.run("black", "noxfile.py")


@nox.session()
def isort(session: nox.Session) -> None:
    """Sort imports."""
    session.install("isort")
    session.run("isort", "--profile", "black", "budget/")
    session.run("isort", "--profile", "black", "noxfile.py")

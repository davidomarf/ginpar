"""
    ginpar.utils
    ~~~~~~~~~~~~

    Implements the utilities used across modules in this package.
"""

import click

def unkebab(s):
    return " ".join(s.split("-"))


# ------------------------------ Throw messages ------------------------------ #

def success(m):
    click.secho(m, fg="green")

def error(m):
    click.secho(m, fg="red")

def alert(m):
    click.secho(m, fg="yellow")
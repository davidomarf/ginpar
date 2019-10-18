"""
    ginpar.init
    ~~~~~~~~~~~

    Implements the initialization of a new project.
"""
import click


def init(force, path):
    click.secho("You're initializing", fg="blue")

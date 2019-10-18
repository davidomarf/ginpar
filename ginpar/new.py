"""
    ginpar.new
    ~~~~~~~~~~

    Implements the creation of a new sketch in the project.
"""
import click


def new(sketch, path):
    click.secho("You're in new", fg="blue")

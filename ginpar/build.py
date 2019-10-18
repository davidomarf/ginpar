"""
    ginpar.build
    ~~~~~~~~~~~~

    Implements the generation of the static site.
"""
import click


def build(path):
    click.secho("You're building", fg="blue")

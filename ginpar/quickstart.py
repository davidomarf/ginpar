"""
    ginpar.quickstart
    ~~~~~~~~~~~~~~~~~

    Implements the importing of demo content into a new project.
"""
import click


def quickstart(force, path):
    click.secho("You're quickstarting", fg="blue")

"""
    ginpar.serve
    ~~~~~~~~~~~~

    Implements the serving of the generated content.
"""
import click


def serve(port):
    click.secho("You're serving", fg="blue")

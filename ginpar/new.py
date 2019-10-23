"""New sketch creation command for Ginpar projects.

This module implements the sketch creation command for the ginpar static content
generator.

`new` will read the configuration file in search for `source_path` and
create a new directory in there with the specified name, which by default is
`new-sketch-{n}`.

This directory will contain the two required files with a boilerplate code.

Examples
--------

To create a new sketch `rectangle`::

    ginpar new rectangle

To start a new sketch with the default name `new-sketch-{n}`::

    ginpar new
"""
import click


def new(sketch):
    """Main function of the module. This is what `ginpar new` calls.

    Parameters
    ----------
    sketch : str
        Name of the sketch to create
    """
    click.secho("You're in new", fg="blue")

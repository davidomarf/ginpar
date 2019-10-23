"""Serve command for Ginpar projects.

This module implements the server starting command for the ginpar static content
generator.

`serve` will start a live-reloading server in a specified port.

Examples
--------

To start a new server in the default port `8080`::

    ginpar serve

To start a new server in a custom port::

    ginpar serve --port=3000
    ginpar serve -p=3000

To force the initialization in case there is a directory with the same name
of the project to initialize: 

    ginpar force --force
    ginpar force -f
"""
import click


def serve(port):
    """Main function of the module. This is what `ginpar serve` calls.

    Parameters
    ----------
    port : int
        The port of the server
    """
    click.secho("You're serving", fg="blue")

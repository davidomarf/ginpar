"""Quickstart command for Ginpar projects.

This module implements the quickstart command for the ginpar static content
generator.

`quickstart` will download the contents of the sample repository hosted at
`davidomarf/ginpar-quickstart <https://github.com/davidomarf/ginpar-quickstart>`_
into `./quickstart`.

This is aimed to provide an easier and faster way to start working in a Ginpar
project for people who isn't familiar with static content generators.

Example
-------

To create `./quickstart` and copy the contents of the sample repository::

    ginpar quickstart

If there's another directory named `quickstart`, you can force this command,
removing the existing directory::

    ginpar quickstart --force
    ginpar quickstart -f
"""
import os
import subprocess

import click

from ginpar.utils.echo import success, alert, echo, error
from ginpar.utils.files import try_remove
from ginpar.utils.git import clone_repo, delete_git_files


def quickstart(force):
    """Main function of the module. This is what `ginpar quickstart` calls.

    Parameters
    ----------
    force : bool
        Remove conflicting files when true.
    """

    repo = "davidomarf/ginpar-quickstart"
    path = os.path.abspath("quickstart")

    if force:
        alert("Forcing quickstart. This will replace existent directories and files.\n")
        try_remove("quickstart")
        echo("")

    if os.path.isdir(path):
        error(f"`{path}` already exists.")
        echo("Delete it manually or run `ginpar quickstart -f` to force")
        raise click.Abort()

    if clone_repo(repo, path) == 0:
        if delete_git_files(path) == 0:
            echo(f"\nThe Ginpar sample site is ready.\n")
            echo("Run `cd quickstart` to move to the project directory.")
            echo("Then run `ginpar build` or `ginpar serve` to see it working.")
    else:
        raise click.Abort()

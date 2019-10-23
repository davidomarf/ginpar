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


def clone_repo(repo, path):
    """Clone the contents of a repository in a custom path

    Parameters
    ----------
    repo : str
        GitHub repository as in "{USER}/{REPO}"
    path : str
        Path to clone the repository to
    """

    repo_url = f"https://github.com/{repo}.git"

    echo(f"> Cloning {repo} in `{path}`")
    try:
        subprocess.call(["git", "clone", repo_url, path, "--quiet"])
    except OSError:
        error("You don't have git installed in your machine.")
        echo("Please install git and rerun or download the files manually:")
        echo(f"\t{repo_url}")
        return 1

    success(f"Successfully cloned {repo}.\n")
    return 0


def delete_git_files(path):
    """Delete the git files to only keep the relevant files

    Parameters
    ----------
    path : str
        Path to look for git files
    """

    echo("> Deleting .git files")
    try:
        try_remove(os.path.join(path, ".git"))
        success("Successfully deleted .git files")
    except:
        error(f"Couldn't delete files. Delete all .git files manually in `{path}`")
        return 1

    return 0


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
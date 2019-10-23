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

    ginpar build --path="_site"
"""
import os
import shutil
from pathlib import Path
import sys

import click
from jinja2 import Environment, FileSystemLoader

from ginpar.utils.echo import alert, success, error, info, echo
from ginpar.utils.files import try_remove, copy_folder


_TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")

_THEMES_DIR = os.path.join(Path(os.path.dirname(os.path.abspath(__file__))), "themes")

_SKETCHES_DIR = os.path.join(
    Path(os.path.dirname(os.path.abspath(__file__))), "sketches"
)

_jinja_env = Environment(loader=FileSystemLoader(_TEMPLATES_DIR), trim_blocks=True)


def init_config():
    # TODO: Deprecate this function and clone sample repo instead
    click.secho("\n> Creating `config.json` using template:")
    try:
        config = open("config.json", "r")
    except:
        try:
            config = open("config.json", "w+")
        except:
            error("Failure.")
        else:
            _template = _jinja_env.get_template("config.json.jinja2")
            config.write(_template.render())
            config.close()
            success("Success.")
    else:
        error("Failure. It already exists.")


def quickstart(force):
    """Main function of the module. This is what `ginpar quickstart` calls.

    Parameters
    ----------
    force : bool
        Remove conflicting files when true.
    """

    path = "ginpar-quickstart"

    if force:
        alert("Forcing quickstart. This will replace existent directories and files.")
        try_remove("sketches")
        try_remove("themes")
        try_remove("config.json")
        echo("")

    info(f"Copying demo content into `{os.path.abspath(path)}`")
    copy_folder(_THEMES_DIR, "themes")
    copy_folder(_SKETCHES_DIR, "sketches")
    init_config()  # FIXME Use a copy_file or render_file option imported from utils instead

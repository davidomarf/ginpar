"""
    ginpar.quickstart
    ~~~~~~~~~~~~~~~~~

    Implements the importing of demo content into a new project.
"""
import os
import shutil
from pathlib import Path
import sys

from jinja2 import Environment, FileSystemLoader

from ginpar.utils.echo import alert, success, error, info, echo
from ginpar.utils.files import try_remove, copy_folder

import click


_TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")

_THEMES_DIR = os.path.join(Path(os.path.dirname(os.path.abspath(__file__))), "themes")

_SKETCHES_DIR = os.path.join(
    Path(os.path.dirname(os.path.abspath(__file__))), "sketches"
)

_jinja_env = Environment(loader=FileSystemLoader(_TEMPLATES_DIR), trim_blocks=True)


def init_config():
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


def quickstart(force, path):
    echo("")
    if force:
        alert("Forcing quickstart. This will replace existent directories and files.")
        try_remove("sketches")
        try_remove("themes")
        try_remove("config.json")
        echo("")

    info(f"Copying demo content into `{os.path.abspath(path)}`")
    copy_folder(_THEMES_DIR, "themes")
    copy_folder(_SKETCHES_DIR, "sketches")
    init_config() # FIXME Use a copy_file or render_file option imported from utils instead

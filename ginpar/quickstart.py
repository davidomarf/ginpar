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

from ginpar.utils import alert, success, error, info, echo

import click


_TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")

_THEMES_DIR = os.path.join(Path(os.path.dirname(os.path.abspath(__file__))), "themes")

_SKETCHES_DIR = os.path.join(
    Path(os.path.dirname(os.path.abspath(__file__))), "sketches"
)

_jinja_env = Environment(loader=FileSystemLoader(_TEMPLATES_DIR), trim_blocks=True)


def create_folder(folder):
    echo(f"    > Creating `{folder}`:")
    try:
        os.mkdir(folder)
    except FileExistsError:
        error("    Failure. It already exists.")
    except:
        error("    Failure.")
    else:
        success("    Sucess")


def init_config():
    click.secho("\n  > Creating `config.json` using template:")
    try:
        config = open("config.json", "r")
    except:
        try:
            config = open("config.json", "w+")
        except:
            error("    Failure.")
        else:
            _template = _jinja_env.get_template("config.json.jinja2")
            config.write(_template.render())
            config.close()
            success("    Success.")
    else:
        error("    Failure. It already exists.")


def copy_folder(fr, to):
    echo(f"\n  > Copying `{to}` from `{fr}`:")
    try:
        shutil.copytree(fr, to)
    except FileExistsError:
        error(f"    Failure. It already exists.")
    else:
        success(f"    Success.")


def try_remove(path):
    if os.path.isdir(path):
        echo(f"\n  > `{path}` already exists. Attemping removal:")
        try:
            shutil.rmtree(path)
        except:
            error("    Failure. Restart or delete manually.")
        else:
            success("    Success.")
    elif os.path.isfile(path):
        echo(f"\n  > `{path}` already exists. Attemping removal:")
        try:
            os.remove(path)
        except:
            error(f"    Failure. Restart or delete manually.")
        else:
            success(f"    Success.")
    else:
        info(f"    > `{path}` doesn't exist. Skipping.")


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
    init_config()

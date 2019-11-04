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
import os
import yaml
from datetime import date

import click
from jinja2 import Environment, FileSystemLoader

from ginpar.utils.files import create_folder, create_file
from ginpar.utils.echo import echo, error, success

## TODO: Move read_config into a shared library inside utils
def read_config(path):
    """Create a dictionary out of the YAML file received

    Parameters
    ----------
    path : str
        Path of the YAML file.
    """
    with open(path, "r") as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return config


def new(sketch):
    """Main function of the module. This is what `ginpar new` calls.

    Parameters
    ----------
    sketch : str
        Name of the sketch to create
    """

    _SITE = "config.yaml"
    site = read_config(_SITE)

    path = os.path.join(site["content_path"], sketch)

    _TEMPLATES_DIR = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "templates", "sketch"
    )
    _jinja_env = Environment(loader=FileSystemLoader(_TEMPLATES_DIR), trim_blocks=True)

    if os.path.isdir(path):
        error(f"Failure.")
        echo(f"{path} already exists.")
        raise click.Abort()

    create_folder(path)

    sketch_template = _jinja_env.get_template("sketch.js")
    data_template = _jinja_env.get_template("data.yaml")
    create_file(os.path.join(path, "sketch.js"), sketch_template.render())
    create_file(
        os.path.join(path, "data.yaml"),
        data_template.render(today=date.today().strftime("%Y-%m-%d")),
    )

    echo(f"\nYour new sketch {path} is ready.\n")

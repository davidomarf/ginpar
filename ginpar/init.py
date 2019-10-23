"""Init command for Ginpar projects.

This module implements the initialization command for the ginpar static content
generator.

`init` will prompt for a series of values to write the site configuration file.

Examples
--------

To initialize a project in a standard way to specify the configuration values::

    ginpar init

To skip the prompts and initialize the project with the default values::

    ginpar init --quick
    ginpar init --q

To force the initialization in case there is a directory with the same name
of the project to initialize::

    ginpar force --force
    ginpar force -f
"""

import os

import click
from jinja2 import Environment, FileSystemLoader

from ginpar.utils.echo import info, echo, success, error, alert
from ginpar.utils.files import create_file, create_folder, try_remove
from ginpar.utils.strings import space_to_kebab

_TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
_jinja_env = Environment(loader=FileSystemLoader(_TEMPLATES_DIR), trim_blocks=True)


def prompt_site_config():
    """Echo the prompts and create the configuration dict.

    Echo the instructions and configuration fields, store each input,
    and create a dictionary containing those values.

    Returns
    -------
    dict
        Used to generate the site configuration file.
    """
    info("Welcome to ginpar! We'll ask for some values to initialize your project.")
    echo("")
    sitename = click.prompt("Site name", default="My Site")
    description = click.prompt("Description", default="Cool site")
    author = click.prompt("Author", default="John Doe")
    url = click.prompt("url", default="johndoe.com")
    info("\nIf you're unsure about the next prompts, accept the defaults")
    echo("")
    theme = click.prompt("Theme", default="gart")
    content_path = click.prompt("Sketches path", default="sketches")
    build_path = click.prompt("Build path", default="public")
    return {
        "author": author,
        "sitename": sitename,
        "description": description,
        "url": url,
        "theme": theme,
        "content_path": content_path,
        "build_path": build_path,
    }


def init(force, quick):
    """Main function of the module. This is what `ginpar init` calls.

    Parameters
    ----------
    force : bool
        Remove conflicting files when true.
    
    quick : bool
        Skip prompts when true.
    """
    _config_template = _jinja_env.get_template("config.json.jinja2")

    if force:
        alert("You're forcing the initialization.")
        alert("This will replace any existent file relevant to the project.")
        click.confirm("Do you want to proceed?", abort=True)

    if quick:
        content_path = os.path.join("my-site", "sketches")
        config_json = os.path.join("my-site", "config.json")
        config_dict = _config_template.render()
    else:
        site = prompt_site_config()

        path = space_to_kebab(site["sitename"]).lower()
        print(site["content_path"])
        echo("\n---\n")

        content_path = os.path.join(path, site["content_path"])
        config_json = os.path.join(path, "config.json")
        config_dict = _config_template.render(site)

    if force:
        echo("\n---\n")
        try_remove(content_path)
        try_remove(config_json)
        echo("\n---\n")

    create_folder(content_path)
    create_file(config_json, config_dict)

    echo("\n---\n")
    success(
        "Done!\nRun `ginpar serve` or `ginpar build` and see your new site in action!\n"
    )

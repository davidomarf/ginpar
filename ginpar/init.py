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

    ginpar init --force
    ginpar init -f
"""

import os

import click
import yaml

from ginpar.utils.echo import info, echo, success, error, alert
from ginpar.utils.files import create_file, create_folder, try_remove
from ginpar.utils.strings import space_to_kebab


def prompt_site_config(quick):
    """Echo the prompts and create the configuration dict.

    Echo the instructions and configuration fields, store each input,
    and create a dictionary containing those values.

    Parameters
    ----------
    quick : bool
        Returns the default values immediatle if True.

    Returns
    -------
    dict
        Used to generate the site configuration file.
    """
    site = {
        "author": "David Omar",
        "sitename": "My site",
        "description": "This is a Ginpar project",
        "url": "/",
        "theme": "davidomarf/gart",
        "content_path": "sketches",
        "build_path": "public",
    }

    if quick:
        return site

    info("Welcome to ginpar! We'll ask for some values to initialize your project.")
    echo("")
    site["sitename"] = click.prompt("Site name", default=site["sitename"])
    site["description"] = click.prompt("Description", default=site["description"])
    site["author"] = click.prompt("Author", default=site["author"])
    site["url"] = click.prompt("url", default=site["url"])
    info("\nIf you're unsure about the next prompts, accept the defaults")
    echo("")
    site["theme"] = click.prompt("Theme", default=site["theme"])
    site["content_path"] = click.prompt("Sketches path", default=site["content_path"])
    site["build_path"] = click.prompt("Build path", default=site["build_path"])

    return site


def init(force, quick):
    """Main function of the module. This is what `ginpar init` calls.

    Parameters
    ----------
    force : bool
        Remove conflicting files when true.
    
    quick : bool
        Skip prompts when true.
    """

    if force:
        alert("You're forcing the initialization.")
        alert("This will replace any existent file relevant to the project.")
        click.confirm("Do you want to proceed?", abort=True)

    site = prompt_site_config(quick)
    path = space_to_kebab(site["sitename"]).lower()

    content_path = os.path.join(path, site["content_path"])
    config_yaml = os.path.join(path, "config.yaml")

    echo("\n---\n")

    if force:
        echo("\n---\n")
        try_remove(path)
        echo("\n---\n")

    create_folder(content_path)
    with open(config_yaml, "w") as file:
        yaml.dump(site, file)
        file.write("scripts:\n  p5:\n    https://cdnjs.cloudflare.com/ajax/libs/p5.js/0.9.0/p5.min.js")

    echo("\n---\n")
    success(
        "Done!\nRun `ginpar serve` or `ginpar build` and see your new site in action!\n"
    )

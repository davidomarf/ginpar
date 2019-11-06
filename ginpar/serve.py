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
"""
import click
import yaml
from livereload import Server

from ginpar.build import build

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


def serve(port, watch):
    """Main function of the module. This is what `ginpar serve` calls.

    Parameters
    ----------
    port : int
        The port of the server
    """
    site = read_config("config.yaml")

    build(site["build_path"])

    server = Server()
    server.watch(site["content_path"], "ginpar build")
    if watch:
        server.watch("themes", "ginpar build")
        server.watch("config.yaml", "ginpar build")

    server.serve(port=port, root=site["build_path"])

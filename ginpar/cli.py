"""
    ginpar.cli
    ~~~~~~~~~~

    Implements the command line application to manage ginpar projects.
"""

import click


@click.group()
@click.version_option(message="%(prog)s v%(version)s")
def cli():
    """
    Ginpar is an extra simple static content generator for interactive and parametrisable p5 canvases.
    """
    pass


@cli.command()
@click.option(
    "--path",
    "-p",
    default="public",
    type=click.Path(),
    help="The PATH for the generated site.\nDefault = public",
)
def build(path):
    """Build a static website in PATH"""
    click.secho("Attemping to build the project", fg="blue")

    from ginpar.build import build as ginpar_build

    ginpar_build(path)


@cli.command()
@click.option(
    "--force",
    "-f",
    default=False,
    is_flag=True,
    help="Remove existing directories that may interfere with the initialization",
)
@click.option(
    "--path",
    "-p",
    default="",
    help="The PATH to initialize the project. Defaults to ./",
)
def init(force, path):
    """Initialize a new project in PATH"""
    click.secho("Attemping to initialize a new project", fg="blue")

    from ginpar.init import init as ginpar_init

    ginpar_init(force, path)


@cli.command()
@click.argument("sketch", default="new-sketch")
@click.option(
    "--path",
    "-p",
    default="sketches",
    type=click.Path(),
    help="The path for the newly created sketch",
)
def new(sketch, path):
    """Create a new SKETCH in PATH"""
    click.secho(f"Attemping to create `{sketch}` in `{path}/`", fg="blue")

    from ginpar.new import new as ginpar_new

    ginpar_new(sketch, path)


@cli.command()
@click.option(
    "--force",
    "-f",
    default=False,
    is_flag=True,
    help="Remove existing directories that may interfere the quickstart",
)
@click.option(
    "--path", "-p", default="./", help="The path the demo content will be copied to."
)
def quickstart(force, path):
    """Load a working example in PATH"""
    from ginpar.quickstart import quickstart as ginpar_quickstart

    ginpar_quickstart(force, path)


@cli.command()
@click.option("--port", "-p", default="8080", help="Port for the web server")
def serve(port):
    """Serve the content using PORT"""
    click.secho(f"Trying to initialize a server on port {port}", fg="blue")

    from ginpar.serve import serve as ginpar_serve

    ginpar_serve(port)


if __name__ == "__main__":
    cli()

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
    from ginpar.build import build as ginpar_build

    click.echo("")
    ginpar_build(path)
    click.echo("")


@cli.command()
@click.option(
    "--force",
    "-f",
    default=False,
    is_flag=True,
    help="Remove existing directories that may interfere with the initialization",
)
@click.option(
    "--quick",
    "-q",
    default=False,
    is_flag=True,
    help="Skip the configuration prompts and use the default values",
)
@click.option(
    "--path",
    "-p",
    default="",
    help="The PATH to initialize the project. Defaults to ./",
)
def init(force, path, quick):
    """Initialize a new project in PATH"""
    from ginpar.init import init as ginpar_init

    click.echo("")
    ginpar_init(force, path, quick)
    click.echo("")


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

    click.echo("")
    ginpar_new(sketch, path)
    click.echo("")


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

    click.echo("")
    ginpar_quickstart(force, path)
    click.echo("")


@cli.command()
@click.option("--port", "-p", default="8080", help="Port for the web server")
def serve(port):
    """Serve the content using PORT"""
    from ginpar.serve import serve as ginpar_serve

    click.echo("")
    ginpar_serve(port)
    click.echo("")


if __name__ == "__main__":
    cli()

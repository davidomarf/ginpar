"""Definition of the CLI commands for Ginpar.

This module defines the different commands available for the ginpar static
content generator.

Examples
--------

To get the list of available commands and options run::

    ginpar
"""

import click


@click.group()
@click.version_option(message="%(prog)s v%(version)s")
def cli():
    """
    Ginpar is a static content generator for interactive P5.js sketches,
    awkwardly named after Generative Interactive Parametrisable Canvases.
    """
    pass


@cli.command()
@click.option(
    "--path",
    "-p",
    default="public",
    type=click.Path(),
    help=(
        "The PATH where the site will be built. [ <config.build_path>, public ] "
        "This path is relative to the current directory. When no option is provided "
        "Ginpar will read the <config.build_path> from the configuration file."
    ),
)
def build(path):
    """Build the project content into PATH.

        `ginpar build` will read your configuration file, fetch all the sketches inside
        your <config.content_path>, and build your static site inside PATH, which
        defaults to <config.build_path>, or public if it doesn't exist.

        This operation will wipe all the content from PATH in each run, so you must not
        make modifications you expect to preserve.
    """
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
    help=(
        "If Ginpar finds an existing directory with the same name of the "
        "project being initialized, it'll force its removal. "
        "Only do this if you're completely sure you want to do it."
    ),
)
@click.option(
    "--quick",
    "-q",
    default=False,
    is_flag=True,
    help=(
        "Skip the prompts and use the default values for the configuration file. "
        "You can still modify the variables later by manually updating your "
        "configuration file."
    ),
)
def init(force, quick):
    """Initialize a new project in PATH.

        `ginpar init` will prompt you for a series of values that will be used to
        generate the configuration and file structure of your project.
    """
    from ginpar.init import init as ginpar_init

    click.echo("")
    ginpar_init(force, quick)
    click.echo("")


@cli.command()
@click.argument("sketch")
def new(sketch):
    """Create a new SKETCH.

        `ginpar new` will create a new sketch structure inside your <config.content_path>.

        You must specify the name of the sketch.

        If there's an existing sketch with the same name, it'll throw an error and ask
        for a different name.
    """
    from ginpar.new import new as ginpar_new

    click.echo("")
    ginpar_new(sketch)
    click.echo("")


@cli.command()
@click.option(
    "--force",
    "-f",
    default=False,
    is_flag=True,
    help=(
        "If Ginpar finds an existing directory with the same name of the sample content, "
        "it'll force its removal. "
        "Only do this if you're completely sure you want to do it."
    ),
)
def quickstart(force):
    """Import a working sample project.
    
        `ginpar quickstart` will download the contents of the sample project, hosted
        at github: davidomarf/ginpar-quickstart in the current directory.
    """
    from ginpar.quickstart import quickstart as ginpar_quickstart

    click.echo("")
    ginpar_quickstart(force)
    click.echo("")


@cli.command()
@click.option("--port", "-p", default=8080, help="Port of the server")
@click.option(
    "--watch",
    "-w",
    default=False,
    is_flag=True,
    help=(
        "By default, the server will only watch for changes in the source path, "
        "but if this flag is received, it'll watch all the project directories."
    ),
)
def serve(port, watch):
    """Start a new server in localhost:PORT.

        `ginpar serve` will trigger `ginpar build`, and start a new server inside
        <config.build_path>.

        Every time you modify a file that is part of the project's source code the
        site gets built again.
    """
    from ginpar.serve import serve as ginpar_serve

    click.echo("")
    ginpar_serve(port, watch)
    click.echo("")


if __name__ == "__main__":
    cli()

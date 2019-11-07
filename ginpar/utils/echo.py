"""Echo different categories of messages.

Use either ``click.echo`` or ``click.secho`` with predefined custom
foreground colors to echo different categories of messages like
success, errors, or warnings.
"""

import click


def echo(m):
    """General messages with no emphasis. Blue foreground.
    """
    click.echo(m)


def info(m):
    """Information messages with tips or suggestions. Blue foreground.
    """
    click.secho(m, fg="blue")


def success(m):
    """Success messages after operations or tasks. Green foreground.
    """
    click.secho(m, fg="green")


def error(m):
    """Failure messages that interrumpted a certain operation. Red foreground.
    """
    click.secho(m, fg="red")


def alert(m):
    """Warnings and alerts that may change Ginpar behavior. Yellow foreground.
    """
    click.secho(m, fg="yellow")

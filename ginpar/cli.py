import click

@click.command()
@click.option("--name", "-n", default="new-sketch", help="The name of the sketch")
def new(name):
    click.echo(name)

@click.command()
def cli():
    click.echo("chachacha")
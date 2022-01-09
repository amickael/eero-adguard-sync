import click

from eero_adguard_sync import VERSION
from eero_adguard_sync.commands import sync, clear


@click.group()
@click.version_option(VERSION)
def cli():
    pass


cli.add_command(sync)
cli.add_command(clear)


if __name__ == "__main__":
    cli()

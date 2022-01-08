import click

from eero_adguard_sync import VERSION
from eero_adguard_sync.commands import sync


@click.group()
@click.version_option(VERSION)
def cli():
    pass


cli.add_command(sync)


if __name__ == "__main__":
    cli()

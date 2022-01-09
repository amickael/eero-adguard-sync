import click

from eero_adguard_sync.client import EeroClient


@click.command()
@click.option(
    "--confirm",
    "-y",
    is_flag=True,
    default=False,
    help="Skip interactive confirmation",
)
def clear(confirm: bool = False):
    if not confirm:
        click.confirm("Delete all locally cached credentials?", abort=True)
    EeroClient.clear_credentials()
    click.echo("All locally cached credentials deleted")

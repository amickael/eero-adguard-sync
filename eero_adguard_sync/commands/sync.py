import click
from requests import HTTPError
from timeit import default_timer as timer

from eero_adguard_sync.client import EeroClient, AdGuardClient
from eero_adguard_sync.models import (
    AdGuardCredentialSet,
    AdGuardClientDevice,
    DHCPClientTable,
    DHCPClientTableDiff,
)


NETWORK_SELECT_PROMPT = """Multiple Eero networks found, please select by ID
                
{network_options}

Network ID"""


class EeroAdGuardSyncHandler:
    def __init__(self, eero_client: EeroClient, adguard_client: AdGuardClient):
        self.eero_client = eero_client
        self.adguard_client = adguard_client
        self.__network = self.__prompt_network()

    @property
    def network(self) -> str:
        return self.__network

    def __prompt_network(self) -> str:
        network_list = self.eero_client.account()["networks"]["data"]
        network_count = len(network_list)
        if not network_list:
            raise click.ClickException("No Eero networks associated with this account")
        network_idx = 0
        if network_count > 1:
            network_options = "\n".join(
                [f"{i}: {network['name']}" for i, network in enumerate(network_list)]
            )
            choice = click.Choice([str(i) for i in range(network_count)])
            click.prompt(
                NETWORK_SELECT_PROMPT.format(network_options=network_options),
                type=choice,
                default=str(network_idx),
                show_choices=False,
            )
        network = network_list[network_idx]
        click.echo(f"Selected network '{network['name']}'")
        return network["url"]

    def create(self, diff: DHCPClientTableDiff):
        if not diff.discovered:
            click.echo("No new clients found, skipped creation")
            return
        with click.progressbar(
            diff.discovered, label="Add new clients", show_pos=True
        ) as bar:
            duplicate_devices = []
            for eero_device in bar:
                try:
                    self.adguard_client.add_client_device(
                        AdGuardClientDevice.from_dhcp_client(eero_device)
                    )
                except HTTPError as e:
                    errors = [
                        "client already exists",
                        "another client uses the same id",
                    ]
                    if any(
                        [
                            True
                            for error in errors
                            if error.lower() in e.response.text.lower()
                        ]
                    ):
                        duplicate_devices.append(
                            f"'{eero_device.nickname}' [{eero_device.mac_address}]"
                        )
                    else:
                        raise
            if duplicate_devices:
                for duplicate_device in duplicate_devices:
                    click.secho(
                        f"Skipped device, duplicate name in Eero network: {duplicate_device}",
                        fg="red",
                    )

    def update(self, diff: DHCPClientTableDiff):
        if not diff.associated:
            click.echo("No existing clients found, skipped update")
            return
        with click.progressbar(
            diff.associated, label="Update existing clients", show_pos=True
        ) as bar:
            for adguard_device, eero_device in bar:
                new_device = AdGuardClientDevice.from_dhcp_client(eero_device)
                new_device.params = adguard_device.instance.params
                self.adguard_client.update_client_device(
                    adguard_device.nickname, new_device
                )

    def delete(self, diff: DHCPClientTableDiff):
        if not diff.missing:
            click.echo("No removed clients found, skipped deletion")
            return
        with click.progressbar(
            diff.missing, label="Delete removed clients", show_pos=True
        ) as bar:
            for device in bar:
                self.adguard_client.remove_client_device(device.nickname)

    def sync(self, delete: bool = False, overwrite: bool = False):
        if overwrite:
            self.adguard_client.clear_clients()

        eero_clients = []
        for client in self.eero_client.get_clients(self.__network):
            try:
                eero_clients.append(client.to_dhcp_client())
            except ValueError:
                click.secho(
                    f"Eero device missing MAC address, skipped device named '{client.nickname}'",
                    fg="red",
                )
        eero_table = DHCPClientTable(eero_clients)

        adguard_clients = []
        for client in self.adguard_client.get_clients():
            try:
                adguard_clients.append(client.to_dhcp_client())
            except ValueError:
                click.secho(
                    f"AdGuard device missing MAC address, skipped device named '{client.name}'",
                    fg="red",
                )
        adguard_table = DHCPClientTable(adguard_clients)

        dhcp_diff = adguard_table.compare(eero_table)
        if not overwrite:
            self.update(dhcp_diff)
        self.create(dhcp_diff)
        if delete:
            self.delete(dhcp_diff)


@click.command()
@click.option(
    "--adguard-host",
    help="AdGuard Home host IP address",
    type=str,
)
@click.option(
    "--adguard-user",
    help="AdGuard Home username",
    type=str,
)
@click.option(
    "--adguard-password",
    help="AdGuard Home password",
    type=str,
)
@click.option(
    "--eero-user",
    help="Eero email address or phone number",
    type=str,
)
@click.option(
    "--eero-cookie",
    help="Eero session cookie",
    type=str,
)
@click.option(
    "--delete",
    "-d",
    is_flag=True,
    default=False,
    help="Delete AdGuard clients not found in Eero DHCP list",
)
@click.option(
    "--confirm",
    "-y",
    is_flag=True,
    default=False,
    help="Skip interactive confirmation",
)
@click.option(
    "--overwrite",
    "-o",
    is_flag=True,
    default=False,
    help="Delete all AdGuard clients before sync",
)
def sync(
    adguard_host: str = None,
    adguard_user: str = None,
    adguard_password: str = None,
    eero_user: str = None,
    eero_cookie: str = None,
    delete: bool = False,
    confirm: bool = False,
    overwrite: bool = False,
    *args,
    **kwargs,
):
    # Eero auth
    eero_client = EeroClient(eero_cookie)
    if eero_client.needs_login():
        if not eero_user:
            eero_user = click.prompt("Eero email address or phone number", type=str)
        click.echo("Authenticating Eero...")
        user_token = eero_client.login(eero_user)
        verification_code = click.prompt("Verification code from email or SMS")
        click.echo("Verifying code...")
        eero_client.login_verify(verification_code, user_token)
        click.echo("Eero successfully authenticated")
    else:
        click.echo("Using cached Eero credentials")

    # AdGuard auth
    if not adguard_host:
        adguard_host = click.prompt("AdGuard host IP address", type=str)
    adguard_client = AdGuardClient(adguard_host)
    if not adguard_user:
        adguard_user = click.prompt("AdGuard username", type=str)
    if not adguard_password:
        adguard_password = click.prompt("AdGuard password", type=str, hide_input=True)
    adguard_creds = AdGuardCredentialSet(adguard_user, adguard_password)
    click.echo("Authenticating AdGuard...")
    adguard_client.authenticate(adguard_creds)
    click.echo("AdGuard successfully authenticated")

    # Handle
    handler = EeroAdGuardSyncHandler(eero_client, adguard_client)
    if overwrite:
        delete = False
    if not confirm:
        click.confirm(f"Sync this network?", abort=True)
        if overwrite:
            click.confirm(
                "WARNING: All clients in AdGuard will be deleted, confirm?", abort=True
            )
        if delete:
            click.confirm(
                "WARNING: Clients in AdGuard not found in Eero's DHCP list will be deleted, confirm?",
                abort=True,
            )
    click.echo("Starting sync...")
    start = timer()
    handler.sync(delete, overwrite)
    elapsed = timer() - start
    click.echo(f"Sync complete in {round(elapsed, 2)}s")

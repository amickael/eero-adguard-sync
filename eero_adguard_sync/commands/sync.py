import click
from requests import HTTPError
from timeit import default_timer as timer

from eero_adguard_sync.client import EeroClient, AdGuardClient
from eero_adguard_sync.models import (
    AdGuardCredentialSet,
    EeroClientDevice,
    AdGuardClientDevice,
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

    @staticmethod
    def associate_devices(
        eero_clients: list[EeroClientDevice], adguard_clients: list[AdGuardClientDevice]
    ) -> list[tuple[EeroClientDevice, AdGuardClientDevice]]:
        adguard_client_map = {
            client.normalized_mac: client for client in adguard_clients
        }
        devices = []
        for eero_device in eero_clients:
            adguard_device = adguard_client_map.get(eero_device.normalized_mac)
            if adguard_device:
                pair = (eero_device, adguard_device)
                devices.append(pair)
        return devices

    @staticmethod
    def discover_devices(
        eero_devices: list[EeroClientDevice], adguard_devices: list[AdGuardClientDevice]
    ) -> list[EeroClientDevice]:
        adguard_id_hashes = {device.normalized_mac for device in adguard_devices}
        return [
            device
            for device in eero_devices
            if device.normalized_mac not in adguard_id_hashes
        ]

    @staticmethod
    def prune_devices(
        eero_devices: list[EeroClientDevice], adguard_devices: list[AdGuardClientDevice]
    ) -> list[AdGuardClientDevice]:
        eero_id_hashes = {device.normalized_mac for device in eero_devices}
        return [
            device
            for device in adguard_devices
            if device.normalized_mac not in eero_id_hashes
        ]

    def sync(self, delete: bool = False):
        # Fetch client lists
        eero_devices = self.eero_client.get_clients(self.__network)
        adguard_devices = self.adguard_client.get_clients()

        # Update
        updated_devices = self.associate_devices(eero_devices, adguard_devices)
        for eero_device, adguard_device in updated_devices:
            self.adguard_client.update_client_device(
                adguard_device.name, eero_device.as_adguard_device()
            )

        # Create
        new_clients = self.discover_devices(eero_devices, adguard_devices)
        for eero_device in new_clients:
            try:
                self.adguard_client.add_client_device(eero_device.as_adguard_device())
            except HTTPError as e:
                if e.response.text.strip() == "Client already exists":
                    click.secho(
                        f"Skipped device, duplicate name in Eero network: '{eero_device.nickname}' [{eero_device.mac}]",
                        fg="red",
                    )
                else:
                    raise

        # Delete
        if delete:
            removed_devices = self.prune_devices(eero_devices, adguard_devices)
            for adguard_device in removed_devices:
                self.adguard_client.remove_client_device(adguard_device.name)


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
def sync(
    adguard_host: str = None,
    adguard_user: str = None,
    adguard_password: str = None,
    eero_user: str = None,
    delete: bool = False,
    confirm: bool = False,
    *args,
    **kwargs,
):
    # Eero auth
    eero_client = EeroClient()
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
    if not confirm:
        click.confirm(f"Sync this network?", abort=True)
        if delete:
            click.confirm(
                "WARNING: Clients in AdGuard not found in Eero's DHCP list will be deleted, confirm?",
                abort=True,
            )
    click.echo("Starting sync...")
    start = timer()
    handler.sync(delete)
    elapsed = timer() - start
    click.echo(f"Sync complete in {round(elapsed, 2)}s")

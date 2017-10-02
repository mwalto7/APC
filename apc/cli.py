import sys

import click
from apc.access_point import AccessPoint
from apc.controller import Controller

from apc import fileutil


@click.command()
@click.argument('input_file', type=click.Path())
def cli(input_file):
    """A command line tool to quickly configure access points connected to a wireless controller.

    \b
    :param input_file:
    Excel file with a .xlsx extension containing at least two columns, named "MAC Address"
    and "Name/Location". The "Name/Location" column is required, but only needs a value if
    the AP to be configured has already been named. If the AP has not yet been named
    (i.e. the AP has its default name, such as AP0EF23.2F56.CDE1), its default name is
    automatically generated from the AP's provided MAC address and used in the configuration
    commands. The MAC addresses are required for all APs to be configured.
    """

    # Ensure input file exists and has correct file extension
    try:
        xl = fileutil.ensure_path(input_file)
    except FileExistsError as e:
        click.secho(str(e), fg='red', bold=True)
        sys.exit(0)
    except ValueError as e:
        click.secho(str(e), fg='red', bold=True)
        sys.exit(0)

    # Parse input file
    df = xl.parse()
    macs = [str(mac) for mac in df['MAC Address']]
    names = [str(name) for name in df['Name/Location']]
    aps = [AccessPoint(names[i], macs[i]) for i in range(len(df))]

    wlc = Controller()
    with wlc.connection as session:

        # Rename APs
        if click.confirm('Do you want to rename the AP(s)?', default=False):
            with click.progressbar(aps, label='Name/Location', show_eta=False) as bar:
                for ap in bar:
                    if ap.is_connected(wlc):
                        ap.rename(session)
                        ap.set_location(session)
                    else:
                        click.secho(f'\n{ap} is not connected to {wlc}\n', fg='red', bold=True)

        # Configure primary controller
        if click.confirm('Do you want to configure the primary controller?', default=False):
            primary_controller = click.prompt('\nPrimary controller name')
            primary_ip = click.prompt('Primary controller IP')
            with click.progressbar(aps, label='Primary controller', show_eta=False) as bar:
                for ap in bar:
                    if ap.is_connected(wlc):
                        ap.set_primary_controller(session, primary_controller, primary_ip)
                    else:
                        click.secho(f'{ap} is not connected to {wlc}\n', fg='red', bold=True)

        # Configure AP mode
        if click.confirm('Do you want to configure the AP mode?', default=False):
            mode = click.prompt('\nEnter the AP mode', type=click.Choice(AccessPoint.modes))
            with click.progressbar(aps, label='AP mode', show_eta=False) as bar:
                for ap in bar:
                    if ap.is_connected(wlc):
                        ap.set_mode(session, mode)
                    else:
                        click.secho(f'{ap} is not connected to {wlc}\n', fg='red', bold=True)

        # Configure AP group
        if click.confirm('Do you want to configure the AP group?', default=False):
            group = click.prompt('\nEnter the AP group name', type=click.Choice(AccessPoint.groups))
            with click.progressbar(aps, label='AP group', show_eta=False) as bar:
                for ap in bar:
                    if ap.is_connected(wlc):
                        ap.set_group(session, group)
                    else:
                        click.secho(f'{ap} is not connected to {wlc}\n', fg='red', bold=True)

        click.secho('\nConfiguration complete. Wait for APs to reboot.', fg='green', bold=True)

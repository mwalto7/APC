import click

from apc import fileutil


@click.argument('input_file', type=click.Path(exists=True))
@click.version_option('1.0')
def cli(input_file, output_file):
    """This script allows quick configuration of Cisco access points from the command line."""

    df = fileutil.process_excel_file(input_file)

    mac_addresses = [str(x) for x in df['MAC Address']]
    default_names = [str(x) for x in df['Default Name']]
    new_names = [str(x) for x in df['New Name/Location']]

    controller = Controller()

    # Establish connection to controller
    with controller.connect() as session:

        # Configure name/location
        with click.progressbar(mac_addresses, label='Renaming', show_eta=False) as bar:
            for mac_address in bar:
                click.echo(f'\t{mac_address}')

                curr_index = mac_addresses.index(mac_address)
                default_name = default_names[curr_index]
                new_name = new_names[curr_index]

                ap_name = default_name if new_name == 'nan' else new_name
                rename_output = rename_ap(session, ap_name, mac_address)
                location_output = set_ap_location(session, ap_name)

        # Configure primary controller
        with click.progressbar(default_names, label='Configuring primary controller', show_eta=False) as bar:

            primary_controller_name = click.prompt('Primary Controller Name')
            primary_controller_ip = click.prompt('Primary Controller IP')

            for ap_name in bar:
                curr_index = default_names.index(ap_name)
                default_name = default_names[curr_index]
                new_name = new_names[curr_index]

                ap_name = default_name if new_name == 'nan' else new_name
                click.echo(f'\t{ap_name}')
                output = set_primary_controller(session, primary_controller_name, primary_controller_ip, ap_name)

        # Configure AP mode
        with click.progressbar(default_names, label='Configuring AP mode', show_eta=False) as bar:

            ap_modes = ['Local', 'bridge', 'flex+bridge', 'flexconnect', 'monitor', 'reap', 'rogue',
                        'se-connect',
                        'sniffer']
            ap_mode = click.prompt('Enter the AP mode', type=click.Choice(ap_modes))

            for ap_name in bar:
                curr_index = default_names.index(ap_name)
                default_name = default_names[curr_index]
                new_name = new_names[curr_index]

                ap_name = default_name if new_name == 'nan' else new_name
                click.echo(f'\t{ap_name}')
                output = set_ap_mode(session, ap_mode, ap_name)

        # Configure AP group
        with click.progressbar(default_names, label='Configuring AP group', show_eta=False) as bar:

            group_names = ['default-group', 'ClearPass', 'MDNS_1', 'MDNS_2', 'RLAN_CSC_VLAN_101', 'high-density',
                           'lsu-default', 'mesh', 'radiustest', 'rftest']
            group_name = click.prompt('Enter the AP group name', type=click.Choice(group_names))

            for ap_name in bar:
                curr_index = default_names.index(ap_name)
                default_name = default_names[curr_index]
                new_name = new_names[curr_index]

                ap_name = default_name if new_name == 'nan' else new_name
                click.echo(f'\t{ap_name}')
                output = set_ap_group(session, group_name, ap_name)

        click.echo(f'\nConfiguration complete. Closing connection to {session.ip}')

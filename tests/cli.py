import click

import fileutil


@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.version_option('1.0')
def cli(input_file):
    """This script allows quick configuration of Cisco access points from the command line."""

    df = fileutil.process_excel_file(input_file)

    mac_addresses = [str(x) for x in df['MAC Address']]
    default_names = [str(x) for x in df['Default Name']]
    new_names = [str(x) for x in df['New Name/Location']]

    ap_names = []
    for i in range(len(df)):
        ap_names.append((default_names[i], new_names[i]))

    controller = Controller()

    # Establish connection to controller
    with controller.connect() as session:

        # # Configure name/location
        # with click.progressbar(mac_addresses, label='Renaming', show_eta=False) as bar:
        #     for mac_address in bar:
        #         click.echo(f'\t{mac_address}')
        #
        #         curr_index = mac_addresses.index(mac_address)
        #         default_name = default_names[curr_index]
        #         new_name = new_names[curr_index]
        #
        #         ap_name = default_name if new_name == 'nan' else new_name
        #         rename_output = rename_ap(session, ap_name, mac_address)
        #         location_output = set_ap_location(session, ap_name)
        #
        #         click.echo(rename_output.strip('\n'))
        #         click.echo(location_output.strip('\n'))

        # Configure primary controller
        primary_controller_name = click.prompt('Primary Controller Name')
        primary_controller_ip = click.prompt('Primary Controller IP')
        with click.progressbar(ap_names, label='Configuring primary controller', show_eta=False) as bar:
            for ap_name in bar:
                curr_index = ap_names.index(ap_name)
                output1 = set_primary_controller(session, primary_controller_name,
                                                 primary_controller_ip, ap_names[curr_index][0])
                output2 = set_primary_controller(session, primary_controller_name,
                                                 primary_controller_ip, ap_names[curr_index][1])

                if output1 == '':
                    click.echo(f'\n{ap_names[curr_index][0]}: Primary Controller Configured')
                else:
                    click.echo(f'\n{ap_names[curr_index][0]}: {output1}')

                if output2 == '':
                    click.echo(f'{ap_names[curr_index][1]}: Primary Controller Configured\n')
                else:
                    click.echo(f'{ap_names[curr_index][1]}: {output2}\n')

        # # Configure AP mode
        # with click.progressbar(default_names, label='Configuring AP mode', show_eta=False) as bar:
        #
        #     ap_modes = ['Local', 'bridge', 'flex+bridge', 'flexconnect', 'monitor', 'reap', 'rogue',
        #                 'se-connect',
        #                 'sniffer']
        #     ap_mode = click.prompt('Enter the AP mode', type=click.Choice(ap_modes))
        #
        #     for ap_name in bar:
        #         curr_index = default_names.index(ap_name)
        #         default_name = default_names[curr_index]
        #         new_name = new_names[curr_index]
        #
        #         ap_name = default_name if new_name == 'nan' else new_name
        #         click.echo(f'\t{ap_name}')
        #         output = set_ap_mode(session, ap_mode, ap_name)
        #
        #         click.echo(output.strip('\n'))
        #
        # # Configure AP group
        # with click.progressbar(default_names, label='Configuring AP group', show_eta=False) as bar:
        #
        #     group_names = ['default-group', 'ClearPass', 'MDNS_1', 'MDNS_2', 'RLAN_CSC_VLAN_101', 'high-density',
        #                    'lsu-default', 'mesh', 'radiustest', 'rftest']
        #     group_name = click.prompt('Enter the AP group name', type=click.Choice(group_names))
        #
        #     for ap_name in bar:
        #         curr_index = default_names.index(ap_name)
        #         default_name = default_names[curr_index]
        #         new_name = new_names[curr_index]
        #
        #         ap_name = default_name if new_name == 'nan' else new_name
        #         click.echo(f'\t{ap_name}')
        #         output = set_ap_group(session, group_name, ap_name)
        #
        #         click.echo(output.strip('\n'))

        click.echo(f'\nConfiguration complete. Closing connection to {session.ip}\n')


# @click.command(options_metavar='[-agmn]')
# @click.option('-a', '--all', is_flag=True, help='Run all configuration commands.')
# @click.option('-c', '--controller', is_flag=True, help='Configure primary controller.')
# @click.option('-g', '--group', is_flag=True, help='Configure AP group.')
# @click.option('-m', '--mode', is_flag=True, help='Configure AP mode.')
# @click.option('-r', '--rename', is_flag=True, help='Rename APs.')
# @click.help_option()
# @click.version_option(version='1.0')
# @click.argument('input_file', type=click.Path(exists=True))
# @click.argument('output_file', type=click.Path(exists=True), required=False)
# def cli(all, controller, group, mode, rename, input_file, output_file):
#     """This script allows quick configuration of Cisco access points from the command line."""
#
#     input_path = os.path.abspath(input_file)
#
#     if output_file is not None:
#         output_path = os.path.abspath(output_file)
#         df = fileutil.process_excel_file(input_path, output_path)
#     else:
#         if click.confirm(f'No output path specified. Are you sure you want to modify {input_file}?', abort=True):
#             df = fileutil.process_excel_file(input_path)
#
#     mac_addresses = [str(x) for x in df['MAC Address']]
#     default_names = [str(x) for x in df['Default Name']]
#     new_names = [str(x) for x in df['New Name/Location']]
#
#     # Establish connection to controller
#     connection = ssh.login()
#     ip = connection.ip
#     username = connection.username
#     password = connection.password
#
#     # Configure name/location
#     if rename is True or all is True:
#         with click.progressbar(mac_addresses, label='Configuring name/location', show_eta=False) as bar:
#             for mac_address in bar:
#                 click.echo(f'\t{mac_address}')
#                 curr_index = mac_addresses.index(mac_address)
#
#                 if new_names[curr_index] != 'nan':
#                     ap_name = new_names[curr_index]
#                 else:
#                     ap_name = default_names[curr_index]
#
#                 rename_output = (commands.rename_ap(connection, ap_name, mac_address))
#                 if rename_output == '\n':
#                     click.secho('AP successfully renamed', fg='green')
#                 else:
#                     click.secho(rename_output, bold=True)
#
#                 location_output = commands.set_ap_location(connection, ap_name)
#                 if location_output == '\n':
#                     click.secho('Location successfully updated', fg='green')
#                 else:
#                     click.secho(location_output, bold=True)
#
#     # Configure primary controller
#     if controller is True or all is True:
#         primary_controller = click.prompt('Primary Controller Name')
#         primary_controller_ip = click.prompt('Primary Controller IP')
#
#         with click.progressbar(default_names, label='Configuring primary controller', show_eta=False) as bar:
#             for ap_name in bar:
#                 curr_index = default_names.index(ap_name)
#
#                 if new_names[curr_index] != 'nan':
#                     ap_name = new_names[curr_index]
#
#                 click.echo(f'\t{ap_name}')
#                 output = commands.set_primary_controller(connection, primary_controller, primary_controller_ip, ap_name)
#                 if output == '\n':
#                     click.secho('Primary controller configured', fg='green')
#                 else:
#                     click.secho(output, bold=True)
#
#     # Configure AP mode
#     if mode is True or all is True:
#         ap_modes = ['Local', 'bridge', 'flex+bridge', 'flexconnect', 'monitor', 'reap', 'rogue',
#                     'se-connect',
#                     'sniffer']
#         ap_mode = click.prompt('Enter the AP mode', type=click.Choice(ap_modes))
#         with click.progressbar(default_names, label='Configuring AP mode', show_eta=False) as bar:
#             for ap_name in bar:
#                 curr_index = default_names.index(ap_name)
#
#                 if new_names[curr_index] != 'nan':
#                     ap_name = new_names[curr_index]
#
#                 click.echo(f'\t{ap_name}')
#                 output = commands.set_ap_mode(connection, ap_mode, ap_name)
#                 click.secho(output, bold=True)
#
#     # Configure AP group
#     if group is True or all is True:
#         group_names = ['default-group', 'ClearPass', 'MDNS_1', 'MDNS_2', 'RLAN_CSC_VLAN_101', 'high-density',
#                        'lsu-default', 'mesh', 'radiustest', 'rftest']
#         group_name = click.prompt('Enter the AP group name', type=click.Choice(group_names))
#         with click.progressbar(default_names, label='Configuring AP group', show_eta=False) as bar:
#             for ap_name in bar:
#                 curr_index = default_names.index(ap_name)
#
#                 if new_names[curr_index] != 'nan':
#                     ap_name = new_names[curr_index]
#
#                 click.echo(f'\t{ap_name}')
#                 output = commands.set_ap_group(connection, group_name, ap_name)
#                 click.secho(output, bold=True)

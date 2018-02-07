import click

from apc.controller import Controller


class AccessPoint:
    """Class that models a Cisco access point."""

    groups = [
        'default-group', 'ClearPass', 'MDNS_1', 'MDNS_2', 'RLAN_CSC_VLAN_101', 'high-density',
        'lsu-default', 'mesh', 'radiustest', 'rftest'
    ]

    modes = ['Local', 'bridge', 'flex+bridge', 'flexconnect', 'monitor', 'reap', 'rogue', 'se-connect', 'sniffer']

    def __init__(self, name=None, mac=None):
        """
        Return a new AP object.
        :param name: desired name for access point
        :param mac: MAC address of access point
        """
        self.mac = mac
        self.default_name = self.__set_default_name()
        self.name = self.default_name if name == 'nan' else name

    def __set_default_name(self):
        """
        Create default AP name from MAC address.
        :return: generated default name if MAC address is not None, else None
        """
        if self.mac is not None:
            mac_split = ''.join(self.mac.split(':'))
            return 'AP' + '.'.join(mac_split[x:x + 4] for x in range(0, len(mac_split), 4)).upper()
        else:
            return None

    def is_connected(self, controller):
        """
        Determine if the AP is connected to the specified controller.
        :param controller: the specified controller
        :return: True if the AP is connected, else False
        """
        return controller.find(self.name) or controller.find(self.default_name)

    def rename(self, connection):
        """
        Configure the AP's name.
        :param connection: connection to send command over
        :return: output of the command
        """
        command = f'config ap name {self.name or self.default_name} {self.mac}'
        try:
            output = connection.send_command(command)
        except:
            click.secho(f'Could not set name for {self}', fg='red')
        else:
            return output

    def set_location(self, connection):
        """
        Configure the AP's location.
        :param connection: connection to send command over
        :return: output of the command
        """
        command = f'config ap location {self.name} {self.name or self.default_name}'
        try:
            output = connection.send_command(command)
        except:
            click.secho(f'Could not set ap location for {self}', fg='red')
        else:
            return output

    def set_primary_controller(self, connection, primary_controller, primary_ip):
        """
        Configure the AP's primary controller.
        :param connection: connection to send command over
        :param primary_controller: name of the primary controller
        :param primary_ip: IP address of the primary controller
        :return: output of the command
        """
        command = f'config ap primary-base {primary_controller} {self.name or self.default_name} {primary_ip}'
        try:
            output = connection.send_command(command)
        except:
            click.secho(f'Cannot configure primary controller for {self}', fg='red')
        else:
            return output

    def set_group(self, connection, group):
        """
        Configure the AP's group.
        :param connection: connection to send command over
        :param group: name of the group
        :return: output of the command
        """
        config_commands = [f'config ap group-name {group} {self.name or self.default_name}', 'y']
        try:
            output = connection.send_config_set(config_commands)
        except:
            click.secho('Could not set AP group name', fg='red')
        else:
            return output

    def set_mode(self, connection, mode):
        """
        Configure the AP's mode.
        :param connection: connection to send command over
        :param mode: the AP mode
        :return: output of the command
        """
        config_commands = [f'config ap mode {mode} {self.name or self.default_name}', 'y']
        try:
            output = connection.send_config_set(config_commands)
        except:
            click.secho('Could not set AP mode', fg='red')
        else:
            return output

    def __str__(self):
        return f'AP [{self.name or self.default_name or self.mac}]'

    def __repr__(self):
        return f'<AP: {self.mac}>'


if __name__ == '__main__':

    wlc = Controller()
    with wlc.connection as session:

        ap = AccessPoint(name='ap_name', mac='mac_addr')
        if ap.is_connected(wlc):

            click.echo(ap.rename(session))
            click.echo(ap.set_primary_controller(session, 'controller', 'ip'))

            ap_group = click.prompt(click.style('Enter the AP group', bold=True), type=click.Choice(ap.groups))
            click.echo(ap.set_group(session, ap_group))

            ap_mode = click.prompt(click.style('Enter the AP mode', bold=True), type=click.Choice(ap.modes))
            click.echo(ap.set_mode(session, ap_mode))

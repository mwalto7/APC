import click
import bcrypt
import getpass
from netmiko import ConnectHandler


class Controller:
    """Class that models a Cisco wireless controller."""

    login_attempts = 3
    device_type = 'cisco_wlc'

    def __init__(self):
        """Return a Controller object."""
        self.ip = None
        self.connection = self.ssh()

    def ssh(self):
        """
        Establish an SSH connection to the controller.
        :return: ConnectHandler object
        """
        while self.login_attempts > 0:
            self.ip = click.prompt(click.style('Controller IP', bold=True))
            username = click.prompt(click.style('Username', bold=True))
            password = getpass.getpass(click.style('Password: ', bold=True))
            try:
                click.echo(f'\nConnecting to device {self.ip}...')
                self.connection = ConnectHandler(
                    device_type=self.device_type,
                    ip=self.ip,
                    username=username,
                    password=password
                )
            except ValueError:
                self.login_attempts -= 1
                click.secho(
                    f'Incorrect login information, {self.login_attempts} attempts left.\n',
                    fg='red',
                    bold=True
                )
            else:
                click.secho(f'Connection established to device {self.ip}\n', fg='green', bold=True)
                hashed = bcrypt.hashpw(self.connection.password.encode('UTF-8'), bcrypt.gensalt())
                self.connection.password = hashed
                return self.connection
        else:
            click.secho('No more login attempts. Try again later.', fg='red', bold=True)

    def find(self, ap_name):
        """
        Search for AP connected to the controller.
        :param ap_name: name of the AP to search for
        :return: True if specified AP is connected, else False.
        """
        command = f'show ap search {ap_name}'
        try:
            output = self.connection.send_command(command)
        except:
            click.secho(
                '\nMust establish connection to controller before running commands.',
                fg='red',
                bold=True
            )
        else:
            if output.find(ap_name) == -1:
                return False
            else:
                return True

    def __str__(self):
        return f'Controller [{self.ip}]'

    def __repr__(self):
        return f'<Controller [{self.ip}]>'


if __name__ == '__main__':

    ap = click.prompt('Enter the name of an AP')
    wlc = Controller()
    with wlc.connection as session:
        wlc.find(ap)

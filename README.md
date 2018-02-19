# APC
A command line tool to quickly configure access points connected to a
wireless controller.

## Install

**Note:** must have `pip` and `virtualenv` installed.

### Virtualenv
`cd` to the project directory and run the following commands:
```
$ virtualenv venv
$ . venv/bin/activate
(venv) $ pip install --editable .

```
You should now have `(venv)` displayed next to your terminal prompt.
To verify everything is working, run `$ apc --help` to display the help
message. Type `$ deactivate`  when done testing to deactivate the
virtual environment.

## Usage
`$ apc [OPTIONS] INPUT_FILE` <br>

**Options:**<br>
`--help` Shows the help message then exits.

**Arguments:**<br>
`INPUT_FILE` must be an Excel file with a *.xlsx* extension
containing at least two columns, named "MAC Address" and
"Name/Location". Values within the "Name/Location" column are needed
only if the APs to be configured have already been named or the
APs are to be renamed using APC. Otherwise, the program generates the
AP's default name based on its MAC address and passes the default name
to the configuration commands.

**Commands:**<br>
Available configuration commands are:<br>
1. Configure AP name and location
2. Configure AP primary controller
3. Configure AP mode
4. Configure AP group name

The user is prompted whether or not to execute individual commands.
The default option for each command is false and is indicated by `N`.
Simply press `enter` to skip a command or type `y` and hit `enter` to
execute the command.

## Example
    $ apc test-aps.xlsx
    Controller IP: <ipaddr>
    Username: user
    Password: pass

    Connecting to device <ipaddr>...
    Connection established to device <ipaddr>

    Do you want to rename the AP(s)? [y/N]: y
    Name/Location  [####################################]  100%
    Do you want to configure the primary controller? [y/N]: y

    Primary controller name: <wlc_name>
    Primary controller IP: <ipaddr>
    Primary controller  [####################################]  100%
    Do you want to configure the AP mode? [y/N]: y

    Enter the AP mode: flexconnect
    AP mode  [####################################]  100%
    Do you want to configure the AP group? [y/N]: y

    Enter the AP group name: default
    AP group  [####################################]  100%

    Configuration complete. Wait for APs to reboot.



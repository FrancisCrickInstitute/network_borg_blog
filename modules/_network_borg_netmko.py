#!/usr/bin/env python3

# Python3 script to get and scrape Cisco IOS configuration using NetMiko

__author__      = 'Paul Mahan, Francis Crick Institute, London UK'
__copyright__   = 'None. Enjoy :-)'

# Use Netmiko to send commands to host
from netmiko.ssh_exception import NetMikoTimeoutException, \
    NetMikoAuthenticationException
from paramiko.ssh_exception import SSHException
from netmiko import ConnectHandler

def netmko (SESSION_TK, YAML_TK, netmko_mode, item, object):

    if SESSION_TK['ARG_debug'] == True:
        print('\n**DEBUG (_network_borg_netmko.py) : Payloads Received:')
        print('SESSION_TK:       ' + str(SESSION_TK))
        print('YAML_TK:          ' + str(YAML_TK))
        print('ITEM:             ' + item)
        print('OBJECT(CMD):      ' + object)
        print('MODE:             ' + netmko_mode)

    # Driver Matrix
    # NAPALM Driver 'ios' = NetMiko Driver 'cisco_ios'
    # NAPALM Driver 'nxos_ssh' = NetMiko Driver 'cisco_nxos'
    if YAML_TK['YAML_driver'] == 'ios':
        driver = 'cisco_ios'
    elif YAML_TK['YAML_driver'] == 'nxos_ssh':
        driver = 'cisco_nxos'

    netmko_log = []
    netmko_dict = []
    netmko_status = False

    # If NetMiko Mode = GET (i.e. send show command)
    if netmko_mode == 'get':
        try:
            while True:
                netmko_log.append(YAML_TK['YAML_fqdn'] + ': [' + item + '] Payload : "' + object + '"')

                net_connect = ConnectHandler (device_type=driver, ip=YAML_TK['YAML_fqdn'], username=SESSION_TK['ENV_user_un'], password=SESSION_TK['ENV_user_pw'])

                net_connect.find_prompt()

                get = net_connect.send_command(object)

                net_connect.disconnect()

                # Capture input error. i.e. command is invalid
                err = '% Invalid'
                if err in get:
                    netmko_log.append(YAML_TK['YAML_fqdn'] + ': [' + item + '] Response "' + object + '" ERR: Invalid Command!')
                    break

                # Response back will be RAW text. By default, Python will return a
                # list of lines in a string and not process breaking at line
                # boundaries. Splitlines sets 'keepends' to true: See:
                # https://docs.python.org/3/library/stdtypes.html#string-methods
                # str.splitlines([keepends])
                netmko_list = get.splitlines()

                for line in netmko_list:
                    stripped = line.strip()
                    netmko_dict.append(stripped)

                netmko_log.append(YAML_TK['YAML_fqdn'] + ': [' + item + '] Response "' + object + '" OK ' + u'\u2714')
                netmko_status = True
                break

        except Exception as e:
            netmko_log.append(YAML_TK['YAML_fqdn'] + ': [' + item + '] Payload "' + object + '" ERR: ' + str(e))
            netmko_status = False

    # If NetMiko Mode = SET (i.e. send configuration command)
    elif netmko_mode == 'set':
        try:
            while True:
                net_connect = ConnectHandler (device_type=driver, ip=YAML_TK['YAML_fqdn'], username=SESSION_TK['ENV_user_un'], password=SESSION_TK['ENV_user_pw'])

                net_connect.find_prompt()

                # Use Send Config Set to Send Command...
                set = net_connect.send_config_set(object)

                # Capture input error. i.e. command is invalid
                err = '% Invalid'
                if err in set:
                    netmko_log.append(YAML_TK['YAML_fqdn'] + ': [' + item + '] Response "' + object + '" ERR: Invalid Command!')
                    break

                # Save Configuration and Disconnect
                net_connect.save_config()
                net_connect.disconnect()

                netmko_status = True
                break

        except Exception as e:
            netmko_log.append(YAML_TK['YAML_fqdn'] + ': [' + item + '] Config Response && : "' + object + '" ERR: ' + str(e))
            netmko_status = False

    else:
        netmko_log.append(YAML_TK['YAML_fqdn'] + ': NetMiko Mode Not Defined!')

    return netmko_status, netmko_log, netmko_dict

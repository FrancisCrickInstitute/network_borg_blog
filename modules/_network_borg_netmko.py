'''
Python3 script to get and scrape Cisco IOS configuration using NetMiko
'''
#!/usr/bin/env python3

__author__ = 'Paul Mahan, Francis Crick Institute, London UK'
__copyright__ = 'None. Enjoy :-)'

# Use Netmiko to send commands to host
from netmiko import ConnectHandler

LOGDIR = '../LOGS/network_borg/'

def netmko(SESSION_TK, YAML_TK, netmko_mode, item, obj):
    '''
    NetMiko Function
    '''

    if SESSION_TK['ARG_debug']: # True
        print('\n**DEBUG (_network_borg_netmko.py) : Payloads Received:')
        print('SESSION_TK:       ' + str(SESSION_TK))
        print('YAML_TK:          ' + str(YAML_TK))
        print('ITEM:             ' + item)
        print('obj(CMD):         ' + obj)
        print('MODE:             ' + netmko_mode)

    # Driver Matrix
    # NAPALM Driver 'ios' = NetMiko Driver 'cisco_ios'
    # NAPALM Driver 'nxos_ssh' = NetMiko Driver 'cisco_nxos'
    # Only IOS uses NetMiko so NX-OS is surplus to requirements but retained
    # for future reference,
    if YAML_TK['YAML_driver'] == 'ios':
        driver = 'cisco_ios'
    elif YAML_TK['YAML_driver'] == 'nxos_ssh':
        driver = 'cisco_nxos'

    netmko_log = []
    netmko_list = []
    netmko_status = False

    # If NetMiko Mode = GET (i.e. send show command)
    if netmko_mode == 'get':
        try:
            while True:
                netmko_log.append(YAML_TK['YAML_fqdn'] + ': - [' + item + \
                    '] Payload : "' + obj + '"')

                # Establish NetMiko device dictionary
                device = {
                    'device_type': driver,
                    'host': YAML_TK['YAML_fqdn'],
                    'username': SESSION_TK['ENV_user_un'],
                    'password': SESSION_TK['ENV_user_pw'],
                    'session_log': LOGDIR + YAML_TK['YAML_fqdn'] + '_' \
                        + item + '_' + netmko_mode + '_netmiko.session.log',
                    #"fast_cli": True, # Shaves 10-seconds. Use with caution
                }

                # Call ConnectionHandler with a variable number of keyword arguments using **
                # Pass in key value pairs individually.
                net_connect = ConnectHandler(**device)

                net_connect.find_prompt()

                net_get = net_connect.send_command(obj)

                net_connect.disconnect()

                # Capture input error. i.e. command is invalid
                err = '% Invalid'
                if err in net_get:
                    netmko_log.append(YAML_TK['YAML_fqdn'] + ': - [' \
                        + item + '] Response "' + obj + '" ERR: Invalid Command!')
                    break

                # Response back will be RAW text. By default, Python will return a
                # list of lines in a string and not process breaking at line
                # boundaries. Splitlines sets 'keepends' to true: See:
                # https://docs.python.org/3/library/stdtypes.html#string-methods
                # str.splitlines([keepends])
                netmko_lines = net_get.splitlines()

                for line in netmko_lines:
                    stripped = line.strip()
                    netmko_list.append(stripped)

                netmko_log.append(YAML_TK['YAML_fqdn'] + ': - [' + item + \
                    '] Response "' + obj + '" OK')
                netmko_status = True
                break

        except Exception as error:
            netmko_log.append(YAML_TK['YAML_fqdn'] + ': - [' + item + \
            '] Payload "' + obj + '" ERR: ' + str(error))
            netmko_status = False

    # If NetMiko Mode = SET (i.e. send configuration command)
    elif netmko_mode == 'set':
        try:
            while True:

                # Establish NetMiko device dictionary
                device = {
                    'device_type': driver,
                    'host': YAML_TK['YAML_fqdn'],
                    'username': SESSION_TK['ENV_user_un'],
                    'password': SESSION_TK['ENV_user_pw'],
                    'session_log': LOGDIR + YAML_TK['YAML_fqdn'] + '_' + item + \
                        '_' + netmko_mode + '_netmiko.session.log',
                    #'fast_cli': True, # Shaves 10-seconds. Use with caution
                }

                # Call ConnectionHandler with a variable number of keyword arguments using **
                net_connect = ConnectHandler(**device)

                net_connect.find_prompt()

                # Use Send Config Set to Send Command...
                net_set = net_connect.send_config_set(obj)

                # Capture input error. i.e. command is invalid
                err = '% Invalid'
                if err in net_set:
                    netmko_log.append(YAML_TK['YAML_fqdn'] + ': - [' + item + \
                        '] Response "' + obj + '" ERR: Invalid Command!')
                    net_connect.disconnect()
                    break

                # Save Configuration and Disconnect
                net_connect.save_config()
                net_connect.disconnect()

                netmko_log.append(YAML_TK['YAML_fqdn'] + ': - [' + item + \
                    '] Response "' + obj + '" OK')
                netmko_status = True
                break

        except Exception as error:
            netmko_log.append(YAML_TK['YAML_fqdn'] + ': - [' + item + \
                '] Config Response && : "' + obj + '" ERR: ' + str(error))
            netmko_status = False

    else:
        netmko_log.append(YAML_TK['YAML_fqdn'] + ': NetMiko Mode Not Defined!')

    return netmko_status, netmko_log, netmko_list

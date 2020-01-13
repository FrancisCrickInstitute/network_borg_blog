#!/usr/bin/env python3
#
# Python3 Network Borg Syncronisation Module

import requests # Required to disable SSH warnings
import json # Required for NXAPI JSON RPC

# Import modules from '/modules' sub-folder within script directory.
# Folder name is significant to Python. '__init__.py' file required in Parent and
# sub-folder(s).
from modules._network_borg_discvry import discvry
from modules._network_borg_getset import getset

# URLLIB3 package to diabled SSH warnings
requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning
)


def sync(SESSION_TK, YAML_TK):

    # Initialise Dictionaries
    sync_log = []
    sync_dict = {}

    # Set Sync Status to False, unless otherwise overwritten.
    sync_status = False

    sync_log.append('\n' + YAML_TK['YAML_fqdn'] + ': SYNC PROCESS STARTED...')


    '''
    DISCOVERY
    '''

    # Call Node Discovery module. Returns Node Version, Model and Netmiko Driver information
    discvry_status, discvry_log, discvry_dict = discvry(SESSION_TK, YAML_TK)

    for line in discvry_log:
        sync_log.append(line)

    # If discovery was successful...
    if discvry_status == True:
        try:
            if SESSION_TK['ARG_debug'] == True:
                print('\n**DEBUG (_network_borg_sync.py) : ' +YAML_TK['YAML_fqdn'] + ' Discovery Dict:')
                print('DISCOVERED:       ' + str(discvry_status))
                print('MODEL:            ' + discvry_dict['MODEL'])
                print('VERSION:          ' + discvry_dict['VERSION'])
                print('GROUP:            ' + discvry_dict['GROUP'])

            else:
                pass


            '''
            GETSET
            '''

            try:
                getset_status, getset_log, getset_template, getset_payload = getset(SESSION_TK, YAML_TK, discvry_dict)

                for line in getset_log:
                    sync_log.append(line)

                if SESSION_TK['ARG_debug'] == True:
                    print('\n**DEBUG (_network_borg_sync.py) : Template (J2) Set:')
                    print(getset_template)
                    print('\n**DEBUG (_network_borg_sync.py) : Payload Set:')
                    print(getset_payload)

            except Exception as e:
                sync_log.append(YAML_TK['YAML_fqdn'] + ': > Failed to GETSET's - ' + str(e))\

            # Even though the sync could have failed, all components completed so
            # mark status as True
            sync_status = True
            sync_log.append(YAML_TK['YAML_fqdn'] + ': SYNC PROCESS COMPLETED :-)')

        except Exception as e:
            sync_log.append(YAML_TK['YAML_fqdn'] + ': SYNC PROCESS ERROR - ' + str(e))
            sync_status = False

    else: # Discovery Status = False
        sync_log.append(YAML_TK['YAML_fqdn'] + ': SYNC PROCESS ERROR - Discovery Failed!')
        sync_status = False


    return sync_status, sync_log

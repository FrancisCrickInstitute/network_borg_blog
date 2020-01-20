#!/usr/bin/env python3
#
# Python3 Network Borg Syncronisation Module

__author__      = 'Paul Mahan, Francis Crick Institute, London UK'
__copyright__   = 'None. Enjoy :-)'

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

# Initialise Global Sync Log List
sync_log = []

# DISCOVERY
# REQ: SESSION_TK, YAML_TK
# RTN: sync_discvry_status, sync_discvry_dict
def sync_discvry(SESSION_TK, YAML_TK):

    sync_log.append(YAML_TK['YAML_fqdn'] + ': DISCOVERY Module Initialised..')
    sync_discvry_dict = {}
    sync_discvry_status = False

    # Call Node Discovery module. Returns Node Version, Model and Netmiko Driver information
    discvry_status, discvry_log, discvry_dict = discvry(SESSION_TK, YAML_TK)

    for line in discvry_log:
        sync_log.append(line)

    # If discovery was successful...
    if discvry_status == True:
        if SESSION_TK['ARG_debug'] == True:
            print('\n**DEBUG (_network_borg_sync.py) : ' + YAML_TK['YAML_fqdn'] + ' Discovery Dict:')
            print('DISCOVERED:       ' + str(discvry_status))
            print('MODEL:            ' + discvry_dict['MODEL'])
            print('VERSION:          ' + discvry_dict['VERSION'])
            print('GROUP:            ' + discvry_dict['GROUP'])

        sync_discvry_status = True
        sync_discvry_dict = discvry_dict

    else:
        sync_discvry_status = False

    return sync_discvry_status, sync_discvry_dict


# GETSET
# REQ: SESSION_TK, YAML_TK, sync_discvry_dict)
# RTN: sync_getset_status, sync_getset_template, sync_getset_payload
def sync_getset(SESSION_TK, YAML_TK, sync_discvry_dict):

    sync_log.append(YAML_TK['YAML_fqdn'] + ': GETSET Module Initialised...')
    sync_getset_template = {}
    sync_getset_payload = {}
    sync_getset_status = False

    getset_status, getset_log, getset_template, getset_payload = getset(SESSION_TK, YAML_TK, sync_discvry_dict)

    for line in getset_log: # Append log to Global Log
        sync_log.append(line)

    if getset_status == True:
        sync_getset_status = True
        sync_getset_template = getset_template
        sync_getset_payload = getset_payload

    else:
        sync_getset_status = False

    if SESSION_TK['ARG_debug'] == True:
        print('\n**DEBUG (_network_borg_sync.py) : GETSET Module Template Set Returned:')
        print(sync_getset_template)
        print('\n**DEBUG (_network_borg_sync.py) : GETSET Module Payload Set Returned:')
        print(sync_getset_payload)

    return sync_getset_status, sync_getset_template, sync_getset_payload

'''
SYNC
'''
def sync(SESSION_TK, YAML_TK):

    sync_status = False

    sync_log.append('\n' + YAML_TK['YAML_fqdn'] + ': SYNC INITIALISED...')

    '''
    CONDITIONAL WORKFLOW...
    '''

    # DISCOVERY
    # REQ: SESSION_TK, YAML_TK
    # RTN: sync_discvry_status, sync_discvry_dict
    sync_discvry_status, sync_discvry_dict = sync_discvry(SESSION_TK, YAML_TK)

    if sync_discvry_status == True:
        sync_log.append(YAML_TK['YAML_fqdn'] + ': DISCVRY Successful')
        # GETSET
        # REQ: SESSION_TK, YAML_TK, sync_discvry_dict)
        # RTN: sync_getset_status, sync_getset_template, sync_getset_payload
        sync_getset_status, sync_getset_template, sync_getset_payload = sync_getset(SESSION_TK, YAML_TK, sync_discvry_dict)

        if sync_getset_status == True:
            sync_log.append(YAML_TK['YAML_fqdn'] + ': GETSET Successful')
            sync_status = True

        else:
            sync_log.append(YAML_TK['YAML_fqdn'] + ': GETSET Failure')
            sync_status = False

    else: # sync_discvry_status == False:
        sync_log.append(YAML_TK['YAML_fqdn'] + ': DISCVRY Failure!')
        sync_status = False
        
    return sync_status, sync_log

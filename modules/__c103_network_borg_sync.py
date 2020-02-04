#!/usr/bin/env python3
#
# Python3 Network Borg Syncronisation Module. Chapter 1.3.

__author__      = 'Paul Mahan, Francis Crick Institute, London UK'
__copyright__   = 'None. Enjoy :-)'

import requests # Required to disable SSH warnings
import json # Required for NXAPI JSON RPC

# Import modules from '/modules' sub-folder within script directory.
# Folder name is significant to Python. '__init__.py' file required in Parent and
# sub-folder(s).
from modules._network_borg_discvry import discvry

# URLLIB3 package to diabled SSH warnings
requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning
)

# DISCOVERY
# REQ: SESSION_TK, YAML_TK
# RTN: sync_discvry_status, sync_discvry_dict
def sync_discvry(SESSION_TK, YAML_TK):

    sync_discvry_log = []

    sync_discvry_log.append(YAML_TK['YAML_fqdn'] + ': > DISCVRY Module Initialised..')
    sync_discvry_dict = {}
    sync_discvry_status = False

    # Call Node Discovery module. Returns Node Version, Model and Netmiko Driver information
    discvry_status, discvry_log, discvry_dict = discvry(SESSION_TK, YAML_TK)

    for line in discvry_log:
        sync_discvry_log.append(line)

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

    return sync_discvry_status, sync_discvry_log, sync_discvry_dict

'''
SYNC
'''
def sync(SESSION_TK, YAML_TK):

    sync_log = [] # Zeroise sync_log per-pass

    sync_status = False
    sync_loop = True

    sync_log.append('\n' + YAML_TK['YAML_fqdn'] + ': SYNC Initialised...')

    '''
    CONDITIONAL WORKFLOW...
    '''

    while sync_loop == True:
        # DISCOVERY
        # REQ: SESSION_TK, YAML_TK
        # RTN: sync_discvry_status, sync_discvry_dict
        sync_discvry_status, sync_discvry_log, sync_discvry_dict = sync_discvry(SESSION_TK, YAML_TK)

        for line in sync_discvry_log:
            sync_log.append(line)

        if sync_discvry_status == True:
            sync_log.append(YAML_TK['YAML_fqdn'] + ': = DISCVRY Module Successful ' + u'\u2714')

        else: # sync_discvry_status == False:
             sync_log.append(YAML_TK['YAML_fqdn'] + ': = DISCVRY Module Failure ' + u'\u2714')
             sync_loop = False

        sync_loop = False # Catch all.

    return sync_status, sync_log

#!/usr/bin/env python3
#
# Python3 Network Borg Syncronisation Module.

__author__      = 'Paul Mahan, Francis Crick Institute, London UK'
__copyright__   = 'None. Enjoy :-)'

import requests # Required to disable SSH warnings
import json # Required for NXAPI JSON RPC

# Import modules from '/modules' sub-folder within script directory. Even though
# the modules are in the same folder as this file, the working directory is one
# level up ../network_borg.py
# Folder name is significant to Python. '__init__.py' file required in Parent and
# sub-folder(s).
from modules._network_borg_discvry import discvry

# URLLIB3 package to diabled SSH warnings
requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning
)

# DISCOVERY
# REQ: SESSION_TK, YAML_TK
# RTN: sync_discvry_status, sync_HOST_TK
def sync_discvry(SESSION_TK, YAML_TK):

    sync_discvry_log = []

    sync_discvry_log.append(YAML_TK['YAML_fqdn'] + ': > DISCVRY Module Initialised..')
    sync_HOST_TK = {}
    sync_discvry_status = False

    # Call Node Discovery module. Returns Node Version, Model and Netmiko Driver information
    discvry_status, discvry_log, HOST_TK = discvry(SESSION_TK, YAML_TK)

    for line in discvry_log:
        sync_discvry_log.append(line)

    # If discovery was successful...
    if discvry_status == True:
        if SESSION_TK['ARG_debug'] == True:
            print('\n**DEBUG (_network_borg_sync.py) : ' + YAML_TK['YAML_fqdn'] + ' Discovery Dict:')
            print('DISCOVERED:       ' + str(discvry_status))
            print('MODEL:            ' + HOST_TK['MODEL'])
            print('VERSION:          ' + HOST_TK['VERSION'])
            print('GROUP:            ' + HOST_TK['GROUP'])

        sync_discvry_status = True
        sync_HOST_TK = HOST_TK

    else:
        sync_discvry_status = False

    return sync_discvry_status, sync_discvry_log, sync_HOST_TK

'''
SYNC
'''
def sync(SESSION_TK, YAML_TK):

    sync_log = [] # Zeroise sync_log per-pass
    sync_wrkflw = True
    sync_status = False

    sync_log.append('\n' + YAML_TK['YAML_fqdn'] + ': SYNC WorkFlow Initialised...')

    '''
    CONDITIONAL WORKFLOW...
    '''
    while sync_wrkflw: # True

        # DISCOVERY
        # REQ: SESSION_TK, YAML_TK
        # RTN: sync_discvry_status, sync_HOST_TK
        sync_discvry_status, sync_discvry_log, sync_HOST_TK = \
            sync_discvry(SESSION_TK, YAML_TK)

        for line in sync_discvry_log:
            sync_log.append(line)

        if not sync_discvry_status: # False
            sync_status = False
            break

        else:
            sync_log.append(YAML_TK['YAML_fqdn'] + ': = DISCVRY Module Successful ' + u'\u2714')
            sync_status = True
            break

    return sync_status, sync_log

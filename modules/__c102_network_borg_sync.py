#!/usr/bin/env python3
#
# Python3 Network Borg Syncronisation Module

__author__      = 'Paul Mahan, Francis Crick Institute, London UK'
__copyright__   = 'None. Enjoy :-)'

import requests # Required to disable SSH warnings
import json # Required for NXAPI JSON RPC

# URLLIB3 package to diabled SSH warnings
requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning
)

# Initialise Global Sync Log List
sync_log = []

'''
SYNC
'''
def sync(SESSION_TK, YAML_TK):

    sync_status = False

    sync_log.append('\n' + YAML_TK['YAML_fqdn'] + ': SYNC INITIALISED...')

    return sync_status, sync_log

#!/usr/bin/env python3
#
# Python3 Network Borg Syncronisation Module

import requests # Required to disable SSH warnings
import json # Required for NXAPI JSON RPC

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

    return sync_status, sync_log

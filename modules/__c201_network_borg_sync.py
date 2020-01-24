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
from modules._network_borg_j2rdr import j2rdr

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

# GETSET
# REQ: SESSION_TK, YAML_TK, sync_discvry_dict)
# RTN: sync_getset_status, sync_getset_template, sync_getset_payload
def sync_getset(SESSION_TK, YAML_TK, sync_discvry_dict):

    sync_getset_log = []

    sync_getset_log.append(YAML_TK['YAML_fqdn'] + ': > GETSET Module Initialised...')
    sync_getset_template = {}
    sync_getset_payload = {}
    sync_getset_status = False

    getset_status, getset_log, getset_template, getset_payload = getset(SESSION_TK, YAML_TK, sync_discvry_dict)

    for line in getset_log: # Append log to Global Log
        sync_getset_log.append(line)

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

    return sync_getset_status, sync_getset_log, sync_getset_template, sync_getset_payload

# J2RDR (Template Render)
# REQ: SESSION_TK, YAML_TK, sync_getset_template
# RTN: sync_j2rdr_status, sync_j2rdr_dict
def sync_j2rdr(SESSION_TK, YAML_TK, sync_getset_template):

    sync_j2rdr_log = []

    sync_j2rdr_log.append(YAML_TK['YAML_fqdn'] + ': > J2RDR Module Initialised...')

    # Initialise a j2rdr_dict {}. This will store the item as the key value
    # and the j2rdr_list as an object.
    sync_j2rdr_dict = {}
    sync_j2rdr_status = True

    # Loop over our template_set:
    # template_set = {
    #    'SNMP': <<< IS ITEM
    #        [
    #            {
    #            'TEMPLATE': 'template_n7k_dev_snmp.j2', <<< IS OBJECT within OBJECTS
    #            'VARS': <<< IS OBJECT within OBJECTS
    #                [
    #                    {
    #                    'SNMP_LOC': SESSION_TK['YAML_loc'], #YAML Inventory <<< IS SUB-OBJECT
    #                    'SNMP_SRC': 'Loopback0', <<< IS SUB-OBJECT
    #                    'SNMP_KEY': SESSION_TK['ENV_snmp_key'] #System Enviro Var <<< IS SUB-OBJECT
    #                    }
    #                ]
    #            }
    #        ],


    for item, objects in sync_getset_template.items():

        if sync_j2rdr_status == False: # If status set to False on previous loop. do not proceed!
            break

        # print('ITEM = ' + item)
        # print('OBJECTS = ' + str(objects))
        for object in objects:
            #print('OBJECT = ' + str(object))
            j2rdr_status, j2rdr_log, j2rdr_list = j2rdr(SESSION_TK, YAML_TK, item, object)

            for line in j2rdr_log:
                sync_j2rdr_log.append(line)



            if j2rdr_status == True:
                sync_j2rdr_dict[item] = j2rdr_list
                sync_j2rdr_status = True

            else: # j2rdr_status == False:
                sync_j2rdr_dict[item] = ''
                sync_j2rdr_status = False

    if SESSION_TK['ARG_debug'] == True:
        print('\n**DEBUG (_network_borg_sync.py) : J2RDR Module Dictionary Returned:')
        print(str(sync_j2rdr_dict))

    return sync_j2rdr_status, sync_j2rdr_log, sync_j2rdr_dict

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

            # GETSET
            # REQ: SESSION_TK, YAML_TK, sync_discvry_dict)
            # RTN: sync_getset_status, sync_getset_template, sync_getset_payload
            sync_getset_status, sync_getset_log, sync_getset_template, sync_getset_payload = sync_getset(SESSION_TK, YAML_TK, sync_discvry_dict)

            for line in sync_getset_log:
                sync_log.append(line)

            if sync_getset_status == True:
                sync_log.append(YAML_TK['YAML_fqdn'] + ': = GETSET Module Successful ' + u'\u2714')

                # J2RDR (Template Render)
                # REQ: SESSION_TK, YAML_TK, sync_getset_template
                # RTN: sync_j2rdr_status, sync_j2rdr_dict
                sync_j2rdr_status, sync_j2rdr_log, sync_j2rdr_dict = sync_j2rdr(SESSION_TK, YAML_TK, sync_getset_template)

                for line in sync_j2rdr_log:
                    sync_log.append(line)

                if sync_j2rdr_status == True:
                    sync_log.append(YAML_TK['YAML_fqdn'] + ': = J2RDR Module Successful ' + u'\u2714')

                else: # sync_j2rdr_status == False:
                    sync_log.append(YAML_TK['YAML_fqdn'] + ': = J2RDR Module Failure ' + u'\u2717')
                    sync_loop = False

            else: # sync_getset_status == False:
                sync_log.append(YAML_TK['YAML_fqdn'] + ': = GETSET Module Failure ' + u'\u2714')
                sync_loop = False

        else: # sync_discvry_status == False:
             sync_log.append(YAML_TK['YAML_fqdn'] + ': = DISCVRY Module Failure ' + u'\u2714')
             sync_loop = False

        sync_loop = False # Catch all.

    return sync_status, sync_log

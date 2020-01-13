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
from modules._network_borg_netmko import netmko
from modules._network_borg_nxapi import nxapi
from modules._network_borg_diffgen import diffgen

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

    sync_log.append('\n' + YAML_TK['YAML_fqdn'] + ': SYNC DICOVERY STARTED...')


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


            '''
            GETSET
            '''

            try:
                getset_status, getset_log, getset_template, getset_payload = getset(SESSION_TK, YAML_TK, discvry_dict)

                for line in getset_log:
                    sync_log.append(line)

                if SESSION_TK['ARG_debug'] == True:
                    print('\n**DEBUG (_network_borg_sync.py) : GETSET Template Set:')
                    print(getset_template)
                    print('\n**DEBUG (_network_borg_sync.py) : GETSET Payload Set:')
                    print(getset_payload)

            except Exception as e:
                sync_log.append(YAML_TK['YAML_fqdn'] + ': > Failed to GETSETs - ' + str(e))


            '''
            JINJA2 Render
            '''
            # Initialise a template_dict {}. This will store the item as the key value
            # and the j2rdr_list as an object.
            template_dict = {}

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

            sync_log.append(YAML_TK['YAML_fqdn'] + ': JINJA2 RENDER STARTED...')

            try:
                for item, objects in getset_template.items():
                    #print('ITEM = ' + item)
                    #print('OBJECTS = ' + str(objects))
                    for object in objects:
                        #print('OBJECT = ' + str(object))
                        j2rdr_status, j2rdr_log, j2rdr_list = j2rdr(YAML_TK, item, object)

                        template_dict[item] = j2rdr_list

                        for line in j2rdr_log:
                            sync_log.append(line)

                if SESSION_TK['ARG_debug'] == True:
                    print('\n**DEBUG (_network_borg_sync.py) : J2RDR Dictionary:')
                    print(template_dict)

            except Exception as e:
                sync_log.append(YAML_TK['YAML_fqdn'] + ': > Template (J2) Render Error - ' + str(e))\


            '''
            RESPONSE
            '''

            try:

                response_dict = {}

                if YAML_TK['YAML_driver'] == 'ios': # Cisco IOS
                    netmko_mode = 'get'
                    sync_log.append(YAML_TK['YAML_fqdn'] + ': NETMIKO PAYLOAD (GET) SENT...')

                    # cmd_set List
                    cmd_set = []

                    for item, objects in getset_payload.items():
                        for object in objects:
                            netmko_status, netmko_log, netmko_dict = netmko (SESSION_TK, YAML_TK, netmko_mode, item, object['CMD'])

                            for line in netmko_log: # Append to Master Log
                                sync_log.append(line)

                            if netmko_status == True: # If Payload Valid, add to response_dict {}
                                response_dict[item] = netmko_dict

                    if netmko_status == True: # If Payload Valid, add to response_dict {}
                        response_dict[item] = netmko_dict
                        response_result = True # Response retrieved so set value to True for later logic.

                    else:
                        response_result = False # No Response retrieved so set value to False for later logic.

                elif YAML_TK['YAML_driver'] == 'nxos_ssh': # Cisco NXOS
                    nxapi_mode = 'get'
                    sync_log.append(YAML_TK['YAML_fqdn'] + ': NXAPI PAYLOAD SENT...')

                    for item, objects in getset_payload.items():
                        for object in objects:

                            # Send the payload object to the NXAPI Module. Example object
                            # {'jsonrpc': '2.0', 'method': 'cli_ascii', 'params': {'cmd': 'show run snmp', 'version': 1.2}, 'id': 2}

                            nxapi_status, nxapi_log, nxapi_list = nxapi(SESSION_TK, YAML_TK, nxapi_mode, item, getset_payload[item])

                            for line in nxapi_log: # Append to Master Log
                                sync_log.append(line)

                            if nxapi_status == True: # If Payload Valid, add to response_dict {}
                                response_dict[item] = nxapi_list
                                response_result = True # Response retrieved so set value to True for later logic.

                            else:
                                response_result = False # No Response retrieved so set value to False for later logic.

                else:
                    sync_log.append(YAML_TK['YAML_fqdn'] + ': Driver ' + YAML_TK['YAML_driver'] + ' Not Supported!')
                    response_result = False # No Response retrieved so set value to False for later logic.

                if SESSION_TK['ARG_debug'] == True:
                    print('\n**DEBUG (_network_borg_sync.py) : Response Dictionary:')
                    print(response_dict)

            except Exception as e:
                sync_log.append(YAML_TK['YAML_fqdn'] + ': > Response (GET) Error - ' + str(e))
                response_result = False # No Response retrieved so set value to False for later logic.

            '''
            COMPARE
            '''

            if response_result == True:
                try:
                    sync_log.append(YAML_TK['YAML_fqdn'] + ': COMPARE (DIFF) OPERATION...')

                    # Create a dictionary with the item (SNMP, AAA, NTP) as the key and the
                    # config line as an object
                    diffgen_dict = {}

                    # Use the response_dict as the master. There should be parity between
                    # the template_list and response_list so we could use template_dict
                    # with the same outcome.
                    for item, object in response_dict.items():
                        # Create a diffgen_list []. This will store a list of objects
                        # (config lines)
                        diffgen_list = []

                        # Generate a list of difference between the response_dict {} and
                        # the template_dict {}
                        diffgen_status, diffgen_log, diffgen_add, diffgen_del = diffgen(SESSION_TK, YAML_TK, response_dict[item], template_dict[item], item)

                        # Process our diffgen_*** lists [] and appen
                        for line in diffgen_del:
                            diffgen_list.append('no ' + line)
                        for line in diffgen_add:
                            diffgen_list.append(line)

                        # Add our compiled list of changes to the diffgen_dict {}
                        # with the item as the key value
                        diffgen_dict[item] = diffgen_list

                        for line in diffgen_log:
                            sync_log.append(line)

                    if SESSION_TK['ARG_debug'] == True:
                        print('\n**DEBUG (_network_borg_sync.py) : DIFFGEN Dictionary:')
                        print(diffgen_dict)

                    compare_result = True # Successfully compared so set value to True for later logic.

                except Exception as e:
                    sync_log.append(YAML_TK['YAML_fqdn'] + ': > Compare (DIFF) Error: ' + str(e))

                    compare_result = False # Unsuccessfully compared so set value to False for later logic.

            else: # response_result == Flase so comapre_result can only be False too.
                sync_log.append(YAML_TK['YAML_fqdn'] + ': COMPARE (DIFF) SKIPPED due to RESPONSE Error')
                compare_result = False

            '''
            PUSH
            '''

            if compare_result == True:
                try:
                    sync_log.append(YAML_TK['YAML_fqdn'] + ': PUSH OPERATION...')
                    sync_log.append(YAML_TK['YAML_fqdn'] + ': [Committed Lines Suffixed "&&" | Uncommitted Lines Suffixed "!!"]')

                    if YAML_TK['YAML_driver'] == 'ios': # Cisco IOS

                        netmko_mode = 'set'

                        for item, objects in diffgen_dict.items():

                            if not objects:
                                sync_log.append(YAML_TK['YAML_fqdn'] + ': - [' + item + '] No DIFF Found')

                            else:
                                sync_log.append(YAML_TK['YAML_fqdn'] + ': - [' + item + '] DIFF Found:')

                                for object in objects:
                                    try:
                                        if SESSION_TK['ARG_commit'] == True:
                                            
                                            netmko_status, netmko_log, netmko_dict = netmko (SESSION_TK, YAML_TK, netmko_mode, item, object)

                                            for line in netmko_log:
                                                sync_log.append(line)

                                        else:
                                            sync_log.append(YAML_TK['YAML_fqdn'] + ': - [' + item + '] Config Payload !! : "' + str(object) + '"')

                                    except Exception as e:
                                        sync_log.append(YAML_TK['YAML_fqdn'] + ': [' + item + '] Config Payload ERR : "' + str(object) + '" < RESULT: FAIL ' + str(e))

                    elif YAML_TK['YAML_driver'] == 'nxos_ssh': # Cisco NXOS

                        nxapi_mode = 'set'

                        for item, objects in diffgen_dict.items():

                            if not objects:
                                sync_log.append(YAML_TK['YAML_fqdn'] + ': - [' + item + '] No DIFF Found')

                            else:
                                sync_log.append(YAML_TK['YAML_fqdn'] + ': - [' + item + '] DIFF Found:')

                                for object in objects:
                                    try:
                                        if SESSION_TK['ARG_commit'] == True:

                                            nxapi_status, nxapi_log, nxapi_dict = nxapi (SESSION_TK, YAML_TK, nxapi_mode, item, object)

                                            for line in nxapi_log:
                                                sync_log.append(line)

                                        else: # commit Flag not True so report only
                                            sync_log.append(YAML_TK['YAML_fqdn'] + ': - [' + item + '] Config Payload !! : "' + str(object) + '"')

                                    except Exception as e:
                                        sync_log.append(YAML_TK['YAML_fqdn'] + ': - [' + item + '] Config Payload ERR "' + str(object) + '" < RESULT: FAIL ' + str(e))

                    else:
                        sync_log.append(YAML_TK['YAML_fqdn'] + ': Driver ' + YAML_TK['YAML_driver'] + ' Not Supported!')

                except Exception as e:
                    sync_log.append(YAML_TK['YAML_fqdn'] + ': > Push Error - ' + str(e))

                # Even though the sync could have failed, all components completed so
                # mark status as True
                sync_status = True

                if SESSION_TK['ARG_commit'] == True:
                    sync_log.append(YAML_TK['YAML_fqdn'] + ': SYNC PROCESS COMPLETED ' + '\U0001f600')
                else:
                    sync_log.append(YAML_TK['YAML_fqdn'] + ': SYNC PROPOSAL GENERATED ' + '\U0001f600')

            else: # comapare_result == False so sync_status can only be False too.
                sync_status = False

        except Exception as e:
                sync_log.append(YAML_TK['YAML_fqdn'] + ': SYNC PROCESS ERROR - ' + str(e))
                sync_status = False

    else: # Discovery Status = False
        sync_log.append(YAML_TK['YAML_fqdn'] + ': SYNC PROCESS ERROR - Discovery Failed!')
        sync_status = False

    return sync_status, sync_log

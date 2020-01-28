'''
Network Borg Sync (Workflow) Module
'''
#!/usr/bin/env python3
#
# Python3 Network Borg Syncronisation Module

__author__ = 'Paul Mahan, Francis Crick Institute, London UK'
__copyright__ = 'None. Enjoy :-)'

import requests # Required to disable SSH warnings

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


def sync_discvry(SESSION_TK, YAML_TK):
    '''
    DISCOVERY
    REQ: SESSION_TK, YAML_TK
    RTN: sync_discvry_status, sync_discvry_dict
    '''
    sync_discvry_log = []

    sync_discvry_log.append(YAML_TK['YAML_fqdn'] + ': > DISCVRY Module Initialised..')
    sync_discvry_dict = {}
    sync_discvry_status = False

    # Call Node Discovery module. Returns Node Version, Model and Netmiko Driver information
    discvry_status, discvry_log, discvry_dict = discvry(SESSION_TK, YAML_TK)

    for line in discvry_log:
        sync_discvry_log.append(line)

    # If discovery was successful...
    if discvry_status: # True
        if SESSION_TK['ARG_debug']: # True
            print('\n**DEBUG (_network_borg_sync.py) : ' + YAML_TK['YAML_fqdn'] + \
                ' Discovery Dict:')
            print('DISCOVERED:       ' + str(discvry_status))
            print('MODEL:            ' + discvry_dict['MODEL'])
            print('VERSION:          ' + discvry_dict['VERSION'])
            print('GROUP:            ' + discvry_dict['GROUP'])

        sync_discvry_status = True
        sync_discvry_dict = discvry_dict

    else:
        sync_discvry_status = False

    return sync_discvry_status, sync_discvry_log, sync_discvry_dict

def sync_getset(SESSION_TK, YAML_TK, sync_discvry_dict):
    '''
    GETSET
    REQ: SESSION_TK, YAML_TK, sync_discvry_dict)
    RTN: sync_getset_status, sync_getset_template, sync_getset_payload
    '''
    sync_getset_log = []

    sync_getset_log.append(YAML_TK['YAML_fqdn'] + ': > GETSET Module Initialised...')
    sync_getset_template = {}
    sync_getset_payload = {}
    sync_getset_status = False

    getset_status, getset_log, getset_template, getset_payload = \
        getset(SESSION_TK, YAML_TK, sync_discvry_dict)

    for line in getset_log: # Append log to Global Log
        sync_getset_log.append(line)

    if getset_status:
        sync_getset_status = True
        sync_getset_template = getset_template
        sync_getset_payload = getset_payload

    else:
        sync_getset_status = False

    if SESSION_TK['ARG_debug']: # True
        print('\n**DEBUG (_network_borg_sync.py) : GETSET Module Template Set Returned:')
        print(sync_getset_template)
        print('\n**DEBUG (_network_borg_sync.py) : GETSET Module Payload Set Returned:')
        print(sync_getset_payload)

    return sync_getset_status, sync_getset_log, sync_getset_template, sync_getset_payload

def sync_j2rdr(SESSION_TK, YAML_TK, sync_getset_template):
    '''
    J2RDR (Template Render)
    REQ: SESSION_TK, YAML_TK, sync_getset_template
    RTN: sync_j2rdr_status, sync_j2rdr_dict
    '''
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

        if not sync_j2rdr_status: # If status set to False on previous loop. do not proceed!
            break

        # print('ITEM = ' + item)
        # print('OBJECTS = ' + str(objects))
        for obj in objects:
            #print('OBJ = ' + str(obj))
            j2rdr_status, j2rdr_log, j2rdr_list = j2rdr(SESSION_TK, YAML_TK, item, obj)

            for line in j2rdr_log:
                sync_j2rdr_log.append(line)

            if j2rdr_status:
                sync_j2rdr_dict[item] = j2rdr_list
                sync_j2rdr_status = True

            else: # j2rdr_status == False:
                sync_j2rdr_dict[item] = ''
                sync_j2rdr_status = False

    if SESSION_TK['ARG_debug']:
        print('\n**DEBUG (_network_borg_sync.py) : J2RDR Module Dictionary Returned:')
        print(str(sync_j2rdr_dict))

    return sync_j2rdr_status, sync_j2rdr_log, sync_j2rdr_dict

def sync_getcfg(SESSION_TK, YAML_TK, sync_getset_payload):
    '''
    GETCFG (Current Configuration)
    REQ: SESSION_TK, YAML_TK, sync_getset_payload
    RTN: sync_getcfg_status, sync_getcfg_dict
    '''
    sync_getcfg_log = []

    sync_getcfg_log.append(YAML_TK['YAML_fqdn'] + ': > GETCFG Module Initialised...')

    sync_getcfg_dict = {}
    sync_getcfg_status = True

    if YAML_TK['YAML_driver'] == 'ios': # Cisco IOS
        netmko_mode = 'get'
        sync_getcfg_log.append(YAML_TK['YAML_fqdn'] + ': * IOS NetMiko Method')

        for item, objects in sync_getset_payload.items():
            for obj in objects:

                if not sync_getcfg_status:
                    # If status set to False on previous loop. do not proceed!
                    break

                netmko_status, netmko_log, netmko_list = \
                    netmko(SESSION_TK, YAML_TK, netmko_mode, item, obj['CMD'])

                for line in netmko_log: # Append to Master Log
                    sync_getcfg_log.append(line)

                if netmko_status: # If Payload Valid, add to response_dict {}
                    sync_getcfg_dict[item] = netmko_list
                    sync_getcfg_status = True

                else:
                    sync_getcfg_dict[item] = ''
                    sync_getcfg_status = False

    elif YAML_TK['YAML_driver'] == 'nxos_ssh': # Cisco NXOS
        nxapi_mode = 'get'
        sync_getcfg_log.append(YAML_TK['YAML_fqdn'] + ': * NX-OS NXAPI Method')

        for item, objects in sync_getset_payload.items():
            # print('ITEM = ' + item)
            # print('OBJECTS = ' + str(objects))
            for obj in objects:
                # print('OBJ = ' + str(obj))

                if not sync_getcfg_status:
                    # If status set to False on previous loop. do not proceed!
                    break

                # Send the payload object to the NXAPI Module. Example object
                # {'jsonrpc': '2.0', 'method': 'cli_ascii', 'params':
                #     {'cmd': 'show run snmp', 'version': 1.2}, 'id': 2}
                nxapi_status, nxapi_log, nxapi_list = \
                    nxapi(SESSION_TK, YAML_TK, nxapi_mode, item, sync_getset_payload[item])

                for line in nxapi_log: # Append to Global Log
                    sync_getcfg_log.append(line)

                if nxapi_status: # If Payload Valid, add to response_dict {}
                    sync_getcfg_dict[item] = nxapi_list
                    sync_getcfg_status = True

                else:
                    sync_getcfg_dict[item] = ''
                    sync_getcfg_status = False

    else:
        sync_getcfg_log.append(YAML_TK['YAML_fqdn'] + ':  * Driver ' + \
            YAML_TK['YAML_driver'] + ' Not Supported!')
        sync_getcfg_status = False

    if SESSION_TK['ARG_debug']:
        print('\n**DEBUG (_network_borg_sync.py) : GETCFG Dictionary Returned:')
        print(sync_getcfg_dict)

    return sync_getcfg_status, sync_getcfg_log, sync_getcfg_dict

def sync_diffgen(SESSION_TK, YAML_TK, sync_getcfg_dict, sync_j2rdr_dict):
    '''
    DIFFGEN (Compare)
    REQ: SESSION_TK, YAML_TK, sync_confg_dict, sync_j2rdr_dict
    RTN: sync_confg_status, sync_diffgen_dict
    '''
    sync_diffgen_log = []

    sync_diffgen_log.append(YAML_TK['YAML_fqdn'] + ': > DIFFGEN Module Initialised...')

    # Create a dictionary with the item (SNMP, AAA, NTP) as the key and the
    # config line as an object
    sync_diffgen_dict = {}
    sync_diffgen_status = True

    for item, objects in sync_getcfg_dict.items():
        #print('ITEM = ' + item)
        #print('OBJECTS = ' + str(objects))
        if not sync_diffgen_status: # If status set to False on previous loop. do not proceed!
            break

        # Create a diffgen_list []. This will store a list of objects
        # (config lines)
        diffgen_list = []

        # Generate a list of difference between the response_dict {} and
        # the template_dict {}
        diffgen_status, diffgen_log, diffgen_add, diffgen_del = \
            diffgen(SESSION_TK, YAML_TK, sync_getcfg_dict[item], sync_j2rdr_dict[item], item)

        # Process our diffgen_*** lists [] and appen
        for line in diffgen_del:
            diffgen_list.append('no ' + line)
        for line in diffgen_add:
            diffgen_list.append(line)

        # Add our compiled list of changes to the diffgen_dict {}
        # with the item as the key value
        sync_diffgen_dict[item] = diffgen_list

        for line in diffgen_log:
            sync_diffgen_log.append(line)

        if diffgen_status: # If Payload Valid, add to response_dict {}
            sync_diffgen_dict[item] = diffgen_list
            sync_diffgen_status = True

        else:
            sync_diffgen_dict[item] = ''
            sync_diffgen_status = False

    if SESSION_TK['ARG_debug']:
        print('\n**DEBUG (_network_borg_sync.py) : DIFFGEN Dictionary:')
        print(sync_diffgen_dict)

    return sync_diffgen_status, sync_diffgen_log, sync_diffgen_dict

def sync_push(SESSION_TK, YAML_TK, sync_diffgen_dict):
    '''
    PUSH
    REQ: SESSION_TK, YAML_TK, sync_diffgen_dict
    RTN: sync_push_status
    '''
    sync_push_log = []

    sync_push_status = False

    if YAML_TK['YAML_driver'] == 'ios': # Cisco IOS

        if SESSION_TK['ARG_commit']:
            sync_push_log.append(YAML_TK['YAML_fqdn'] + \
                ': > PUSH Module (IOS NETMIKO) Initialised. Commit Mode && ...')

            netmko_mode = 'set'

            for item, objects in sync_diffgen_dict.items():

                if not objects:
                    sync_push_log.append(YAML_TK['YAML_fqdn'] + ': - [' + item + '] No DIFF Found')

                else:
                    sync_push_log.append(YAML_TK['YAML_fqdn'] + ': - [' + item + '] DIFF Found...')

                for obj in objects:
                    netmko_status, netmko_log, netmko_list = \
                        netmko(SESSION_TK, YAML_TK, netmko_mode, item, obj)

                    for line in netmko_log:
                        sync_push_log.append(line)

                    if netmko_status:
                        sync_push_status = True

                    if netmko_list: # List return will be empty. Nothing to do. PEP8
                        pass

            sync_push_log.append(YAML_TK['YAML_fqdn'] + ': * PUSH Commit Successful')

        else: # SESSION_TK['ARG_commit'] == False:
            sync_push_log.append(YAML_TK['YAML_fqdn'] + \
                ': > PUSH Module (IOS NETMIKO) Initialised. Non-Commit Mode !! ...')

            for item, objects in sync_diffgen_dict.items():
                for obj in objects:
                    sync_push_log.append(YAML_TK['YAML_fqdn'] + \
                        ': - [' + item + '] Config Payload !! : "' + str(obj) + '"')

            sync_push_log.append(YAML_TK['YAML_fqdn'] + ': * PUSH Proposal Generated')

        sync_push_status = True

    elif YAML_TK['YAML_driver'] == 'nxos_ssh': # Cisco NXOS

        if SESSION_TK['ARG_commit']:
            sync_push_log.append(YAML_TK['YAML_fqdn'] + \
                ': > PUSH Module (NX-OS NXAPI) Initialised. Commit Mode && ...')

            nxapi_mode = 'set'

            for item, objects in sync_diffgen_dict.items():

                if not objects:
                    sync_push_log.append(YAML_TK['YAML_fqdn'] + ': - [' + item + '] No DIFF Found')

                else:
                    sync_push_log.append(YAML_TK['YAML_fqdn'] + ': - [' + item + '] DIFF Found...')

                for obj in objects:
                    nxapi_status, nxapi_log, nxapi_list = \
                        nxapi(SESSION_TK, YAML_TK, nxapi_mode, item, obj)

                    for line in nxapi_log:
                        sync_push_log.append(line)

                    if nxapi_status:
                        sync_push_status = True

                    if nxapi_list: # List return will be empty. Nothing to do. PEP8
                        pass

            sync_push_log.append(YAML_TK['YAML_fqdn'] + ': * PUSH Commit Successful')

        else: # SESSION_TK['ARG_commit'] == False:
            sync_push_log.append(YAML_TK['YAML_fqdn'] + \
                ': > PUSH Module (NX-OS NXAPI) Initialised. Non-Commit Mode !! ...')

            for item, objects in sync_diffgen_dict.items():
                for obj in objects:
                    sync_push_log.append(YAML_TK['YAML_fqdn'] + \
                        ': - [' + item + '] Config Payload !! : "' + str(obj) + '"')

            sync_push_log.append(YAML_TK['YAML_fqdn'] + ': * PUSH Proposal Generated')

        sync_push_status = True

    return sync_push_status, sync_push_log

def sync(SESSION_TK, YAML_TK):
    '''
    SYNC
    REQ: SESSION_TK, YAML_TK
    RTN: sync_status, sync_log
    '''
    sync_log = [] # Zeroise sync_log per-pass

    sync_status = False
    sync_loop = True

    sync_log.append('\n' + YAML_TK['YAML_fqdn'] + ': SYNC Initialised...')

    ### CONDITIONAL WORKFLOW...
    while sync_loop: # True
        # DISCOVERY
        # REQ: SESSION_TK, YAML_TK
        # RTN: sync_discvry_status, sync_discvry_dict
        sync_discvry_status, sync_discvry_log, sync_discvry_dict = \
            sync_discvry(SESSION_TK, YAML_TK)

        for line in sync_discvry_log:
            sync_log.append(line)

        if sync_discvry_status: # True
            sync_log.append(YAML_TK['YAML_fqdn'] + ': = DISCVRY Module Successful ' + u'\u2714')

            # GETSET
            # REQ: SESSION_TK, YAML_TK, sync_discvry_dict)
            # RTN: sync_getset_status, sync_getset_template, sync_getset_payload
            sync_getset_status, sync_getset_log, sync_getset_template, sync_getset_payload = \
                sync_getset(SESSION_TK, YAML_TK, sync_discvry_dict)

            for line in sync_getset_log:
                sync_log.append(line)

            if sync_getset_status: # True
                sync_log.append(YAML_TK['YAML_fqdn'] + ': = GETSET Module Successful ' + u'\u2714')

                # J2RDR (Template Render)
                # REQ: SESSION_TK, YAML_TK, sync_getset_template
                # RTN: sync_j2rdr_status, sync_j2rdr_dict
                sync_j2rdr_status, sync_j2rdr_log, sync_j2rdr_dict = \
                    sync_j2rdr(SESSION_TK, YAML_TK, sync_getset_template)

                for line in sync_j2rdr_log:
                    sync_log.append(line)

                if sync_j2rdr_status: # True
                    sync_log.append(YAML_TK['YAML_fqdn'] + \
                        ': = J2RDR Module Successful ' + u'\u2714')

                    # GETCFG (Current Configuration)
                    # REQ: SESSION_TK, YAML_TK, sync_getset_payload
                    # RTN: sync_confg_status, sync_confg_dict
                    sync_getcfg_status, sync_getcfg_log, sync_getcfg_dict = \
                        sync_getcfg(SESSION_TK, YAML_TK, sync_getset_payload)

                    for line in sync_getcfg_log:
                        sync_log.append(line)

                    if sync_getcfg_status: # True
                        sync_log.append(YAML_TK['YAML_fqdn'] + \
                            ': = GETCFG Module Successful ' + u'\u2714')

                        # DIFFGEN (Compare)
                        # REQ: SESSION_TK, YAML_TK, sync_confg_dict, sync_j2rdr_dict
                        # RTN: sync_confg_status, sync_diffgen_dict
                        sync_diffgen_status, sync_diffgen_log, sync_diffgen_dict = \
                            sync_diffgen(SESSION_TK, YAML_TK, sync_getcfg_dict, sync_j2rdr_dict)

                        for line in sync_diffgen_log:
                            sync_log.append(line)

                        if sync_diffgen_status: # True:
                            sync_log.append(YAML_TK['YAML_fqdn'] + \
                                ': = DIFFGEN Module Successful ' + u'\u2714')

                            # PUSH
                            # REQ: SESSION_TK, YAML_TK, sync_diffgen_dict
                            # RTN: sync_push_status
                            sync_push_status, sync_push_log = \
                                sync_push(SESSION_TK, YAML_TK, sync_diffgen_dict)

                            for line in sync_push_log:
                                sync_log.append(line)

                            if sync_push_status:
                                sync_log.append(YAML_TK['YAML_fqdn'] + \
                                    ': = PUSH Module Successful ' + u'\u2714')

                            else: # sync_push_status == False:
                                sync_log.append(YAML_TK['YAML_fqdn'] + \
                                    ': = PUSH Module Failure ' + u'\u2717')
                                sync_loop = False

                        else: # sync_diffgen_status == False:
                            sync_log.append(YAML_TK['YAML_fqdn'] + \
                                ': = DIFFGEN Module Failure ' + u'\u2717')
                            sync_loop = False

                    else: # sync_getcyg_status == False:
                        sync_log.append(YAML_TK['YAML_fqdn'] + \
                            ': = GETCFG Module Failure ' + u'\u2717')
                        sync_loop = False

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

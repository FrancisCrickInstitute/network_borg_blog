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
from modules._network_borg_j2rdr import j2rdr
from modules._network_borg_netmko import netmko
from modules._network_borg_nxapi_garbx import garbx

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
                    for object in objects:
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

                if YAML_TK['YAML_driver'] == 'ios': # NetMiko Driver Cisco IOS
                    netmko_mode = 'get'
                    sync_log.append(YAML_TK['YAML_fqdn'] + ': NETMIKO PAYLOAD (GET) SENT...')

                    for item, objects in getset_payload.items():

                        for object in objects:
                            netmko_status, netmko_log, netmko_dict = netmko (SESSION_TK, YAML_TK, netmko_mode, item, object['CMD'])
                            response_dict[item] = netmko_dict

                            for line in netmko_log:
                                sync_log.append(line)

                elif YAML_TK['YAML_driver'] == 'nxos_ssh': # NetMiko Driver Cisco NXOS

                    sync_log.append(YAML_TK['YAML_fqdn'] + ': NXAPI PAYLOAD SENT...')

                    # Define JSON Payload Header and URL
                    myurl = ('https://' + YAML_TK['YAML_fqdn'] + ':830/ins')
                    myheader={'content-type':'application/json-rpc'}

                    for item, objects in getset_payload.items():
                        for object in objects:

                            response = requests.post(
                                myurl,
                                data=json.dumps(getset_payload[item]),
                                headers=myheader,
                                auth=(SESSION_TK['ENV_user_un'], SESSION_TK['ENV_user_pw']),
                                verify=False
                            ).json()

                        # RESPONSE sent through NXAPI Garburator.
                        stripped_response = garbx(response)

                        response_dict[item] = stripped_response

                    sync_log.append(YAML_TK['YAML_fqdn'] + ': - Response Successful')

                else:
                    sync_log.append(YAML_TK['YAML_fqdn'] + ': NetMiko Driver ' + YAML_TK['YAML_driver'] + ' Not Supported!')

                if SESSION_TK['ARG_debug'] == True:
                    print('\n**DEBUG (_network_borg_sync.py) : Response Dictionary:')
                    print(response_dict)

            except Exception as e:
                sync_log.append(YAML_TK['YAML_fqdn'] + ': > Response (GET) Error - ' + str(e))

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

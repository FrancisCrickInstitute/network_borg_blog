'''
Python3 script to get and scrape Cisco NX-OS configuration using NXAPI
'''
#!/usr/bin/env python3

__author__ = 'Paul Mahan, Francis Crick Institute, London UK'
__copyright__ = 'None. Enjoy :-)'

import json # Required for NXAPI JSON RPC
import requests # Required to disable SSH warnings

from modules._network_borg_nxapi_garbx import garbx

# URLLIB3 package to diabled SSH warnings
requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning
)

def nxapi(SESSION_TK, YAML_TK, nxapi_mode, item, obj):
    '''
    NXAPI Function
    '''

    if SESSION_TK['ARG_debug']: # True
        print('\n**DEBUG (_network_borg_nxapi.py) : Objects Received:')
        print('SESSION_TK:       ' + str(SESSION_TK))
        print('YAML_TK:          ' + str(YAML_TK))
        print('ITEM:             ' + str(item))
        print('OBJECT(CMD):      ' + str(obj))
        print('MODE:             ' + nxapi_mode)

    nxapi_log = []
    nxapi_list = []
    nxapi_status = False

    # Define JSON Payload Header and URL
    myurl = ('https://' + YAML_TK['YAML_fqdn'] + ':830/ins')
    myheader = {'content-type':'application/json-rpc'}

    if nxapi_mode == 'get':

        # Set the NXAPI method to cli_ascii.
        nxapi_method = 'cli_ascii'

        # Example object:
        # [{'CMD': 'show run aaa'}]
        # Extract the value of CMD
        command = obj[0]['CMD']

        # Define payload to be posted via JSON RPC
        get_payload = [
            {
                "jsonrpc": "2.0",
                "method": nxapi_method,
                "params": {
                    "cmd": command,
                    "version": 1.2
                },
                "id": 1
            }
        ]

        try:
            # Send the JSON RPC payload
            get_response = requests.post(
                myurl,
                data=json.dumps(get_payload),
                headers=myheader,
                auth=(SESSION_TK['ENV_user_un'], SESSION_TK['ENV_user_pw']),
                verify=False
            ).json()

            if SESSION_TK['ARG_debug']: # True
                print('RESPONSE:         ' + str(get_response))

            if 'result' in str(get_response): # 'result' implies OK.
                # Example Response - {'jsonrpc': '2.0', 'result': {{'msg': 'CROPPED''}}, 'id': 2}
                # Parse through garbx to clean msg blob
                nxapi_list = garbx(get_response)
                nxapi_log.append(YAML_TK['YAML_fqdn'] + ': - [' + str(item) + \
                    '] Payload (Get) Successful')
                nxapi_status = True

            elif 'error' in str(get_response): # 'error' implies BAD.
                # Example Response - {'jsonrpc': '2.0', 'error': {CROPPED}, 'id': 2}
                nxapi_log.append(YAML_TK['YAML_fqdn'] + ': - [' + str(item) + \
                    '] Payload (Get) Unsuccessful! Reason: "' + \
                    str(get_response['error']['data']['msg'].strip()))
                nxapi_status = False

            else:
                nxapi_log.append(YAML_TK['YAML_fqdn'] + ': - [' + str(item) + \
                    '] Payload (Get) Unhandled ' + str(get_response))
                nxapi_status = False

            return nxapi_status, nxapi_log, nxapi_list

        except Exception as error:
            nxapi_log.append(YAML_TK['YAML_fqdn'] + ': Response Exception ' + str(error))
            nxapi_log.append(YAML_TK['YAML_fqdn'] + \
                ': *** Ensure NXAPI is enabled on ' + YAML_TK['YAML_fqdn'] + ' ***:')
            nxapi_log.append('feature nxapi')
            nxapi_log.append('no nxapi http')
            nxapi_log.append('nxapi https port 830')
            nxapi_log.append('nxapi sandbox')
            nxapi_status = False

            return nxapi_status, nxapi_log, nxapi_list

    elif nxapi_mode == 'set':

        # Set the NXAPI method to cli.
        nxapi_method = 'cli'

        try:
            if SESSION_TK['ARG_commit']: # True

                # Define payload to be posted via JSON RPC
                set_payload = [
                    {
                        "jsonrpc": "2.0",
                        "method": nxapi_method,
                        "params": {
                            "cmd": obj,
                            "version": 1.2
                        },
                        "id": 1
                    }
                ]

                # Send the JSON RPC payload
                set_response = requests.post(
                    myurl,
                    data=json.dumps(set_payload),
                    headers=myheader,
                    auth=(SESSION_TK['ENV_user_un'], SESSION_TK['ENV_user_pw']),
                    verify=False
                ).json()

                if SESSION_TK['ARG_debug']: # True
                    print('RESPONSE:         ' + str(set_response))

                if 'result' in str(set_response):
                    # Example Response - {'jsonrpc': '2.0', 'result': {{'msg': 'CROPPED''}}, 'id': 2}
                    nxapi_log.append(YAML_TK['YAML_fqdn'] + ': - [' + str(item) + \
                        '] Payload (Set) Successful "' + str(obj) + '"')
                    nxapi_status = True

                elif 'error' in str(set_response):
                    # Example Response - {'jsonrpc': '2.0', 'error': {CROPPED}, 'id': 2}
                    nxapi_log.append(YAML_TK['YAML_fqdn'] + ': - [' + str(item) + \
                        '] Payload (Set) Unsuccessful! Reason: "' + str(obj) + \
                        '" ' + str(set_response['error']['data']['msg'].strip()))
                    nxapi_status = False

                else:
                    nxapi_log.append(YAML_TK['YAML_fqdn'] + ': - [' + str(item) \
                        + '] Payload (Set) Unhandled: ' + str(set_response))
                    nxapi_status = False

                # Copy running-config startup-config
                wrm_payload = [
                    {
                        "jsonrpc": "2.0",
                        "method": "cli",
                        "params": {
                            "cmd": "copy running-config startup-config",
                            "version": 1.2
                        },
                        "id": 1
                    }
                ]

                requests.post(
                    myurl,
                    data=json.dumps(wrm_payload),
                    headers=myheader,
                    auth=(SESSION_TK['ENV_user_un'], SESSION_TK['ENV_user_pw']),
                    verify=False
                ).json()

                # Do not log response! It generates lots of output!

                # We've reached the end of our try: statement so status = True
                nxapi_status = True

                return nxapi_status, nxapi_log, nxapi_list

            else: # commit Flag not True so report only
                nxapi_log.append(YAML_TK['YAML_fqdn'] + ': - [' + str(item) + \
                    '] Config Payload !! : "' + str(obj) + '"')
                nxapi_status = False
                return nxapi_status, nxapi_log, nxapi_list

        except Exception as error:
            nxapi_log.append(YAML_TK['YAML_fqdn'] + ': - [' + str(item) + '] \
                Config Payload ERR : "' + str(obj) + '" < RESULT: FAIL ' + str(error))
            nxapi_status = False
            return nxapi_status, nxapi_log, nxapi_list
    else:
        nxapi_log.append(YAML_TK['YAML_fqdn'] + ': NXAPI Mode Invalid')
        nxapi_status = False

    return nxapi_status, nxapi_log, nxapi_list

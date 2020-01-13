#!/usr/bin/env python3

# Python3 script to get and scrape Cisco IOS configuration using NetMiko

__author__      = 'Paul Mahan, Francis Crick Institute, London UK'
__copyright__   = 'None. Enjoy :-)'

import requests # Required to disable SSH warnings
import json # Required for NXAPI JSON RPC

from modules._network_borg_nxapi_garbx import garbx

# URLLIB3 package to diabled SSH warnings
requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning
)

def nxapi (SESSION_TK, YAML_TK, nxapi_mode, item, object):

    if SESSION_TK['ARG_debug'] == True:
        print('\n**DEBUG (_network_borg_nxapi.py) : Payloads Received:')
        print('SESSION_TK:       ' + str(SESSION_TK))
        print('YAML_TK:          ' + str(YAML_TK))
        print('ITEM:             ' + str(item))
        print('OBJECT(CMD):      ' + str(object))
        print('MODE:             ' + nxapi_mode)

    # Driver Matrix
    # NAPALM Driver 'ios' = NetMiko Driver 'cisco_ios'
    # NAPALM Driver 'nxos_ssh' = NetMiko Driver 'cisco_nxos'
    if YAML_TK['YAML_driver'] == 'ios':
        driver = 'cisco_ios'
    elif YAML_TK['YAML_driver'] == 'nxos_ssh':
        driver = 'cisco_nxos'

    nxapi_log = []
    nxapi_list = []
    nxapi_status = False

    # Define JSON Payload Header and URL
    myurl = ('https://' + YAML_TK['YAML_fqdn'] + ':830/ins')
    myheader={'content-type':'application/json-rpc'}

    if nxapi_mode == 'get':

        nxapi_method = 'cli_ascii'
        command = object[0]['CMD']

        payload=[
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
            response = requests.post(
                myurl,
                data=json.dumps(payload),
                headers=myheader,
                auth=(SESSION_TK['ENV_user_un'], SESSION_TK['ENV_user_pw']),
                verify=False
            ).json()

            if SESSION_TK['ARG_debug'] == True:
                print('\n**DEBUG (_network_borg_nxapi.py) : Payload Response:')
                print(str(response))

            if 'result' in str(response):
                # Example Response - {'jsonrpc': '2.0', 'result': {{'msg': 'CROPPED''}}, 'id': 2}
                nxapi_list = garbx(response)
                nxapi_log.append(YAML_TK['YAML_fqdn'] + ': - [' + str(item) + '] Response Successful ' + u'\u2714')
                nxapi_status = True

            elif 'error' in str(response):
                # Example Response - {'jsonrpc': '2.0', 'error': {CROPPED}, 'id': 2}
                nxapi_log.append(YAML_TK['YAML_fqdn'] + ': - [' + str(item) + '] Response Unsuccessful! Reason: "' + str(response['error']['data']['msg'].strip()))
                nxapi_status = False

            else:
                nxapi_log.append(YAML_TK['YAML_fqdn'] + ': - [' + str(item) + '] Response Unhandled ' + str(response))
                nxapi_status = False

            return nxapi_status, nxapi_log, nxapi_list

        except Exception as e:
            nxapi_log.append(YAML_TK['YAML_fqdn'] + ': Response Exception ' + str(e))
            nxapi_log.append(YAML_TK['YAML_fqdn'] + ': *** Ensure NXAPI is enabled on ' + YAML_TK['YAML_fqdn'] + ' ***:')
            nxapi_log.append('feature nxapi')
            nxapi_log.append('no nxapi http')
            nxapi_log.append('nxapi https port 830')
            nxapi_log.append('nxapi sandbox')
            nxapi_status = False

            return nxapi_status, nxapi_log, nxapi_list

    elif nxapi_mode == 'set':

        nxapi_method = 'cli'

        try:
            if SESSION_TK['ARG_commit'] == True:
                nxapi_log.append(YAML_TK['YAML_fqdn'] + ': Config Payload: && "' + str(object) + '"')

                payload=[
                  {
                    "jsonrpc": "2.0",
                    "method": nxapi_method,
                    "params": {
                      "cmd": object,
                      "version": 1.2
                    },
                    "id": 1
                  }
                ]

                response = requests.post(
                    myurl,
                    data=json.dumps(payload),
                    headers=myheader,
                    auth=(SESSION_TK['ENV_user_un'], SESSION_TK['ENV_user_pw']),
                    verify=False
                ).json()

                print('REPOSNSE: ' + str(response))

                if SESSION_TK['ARG_debug'] == True:
                    print('\n**DEBUG (_network_borg_nxapi.py) : Payload Response:')
                    print(str(response))

                if 'result' in str(response):
                    # Example Response - {'jsonrpc': '2.0', 'result': {{'msg': 'CROPPED''}}, 'id': 2}
                    nxapi_log.append(YAML_TK['YAML_fqdn'] + ': - [' + str(item) + '] Response Successful ' + u'\u2714')
                    nxapi_status = True

                elif 'error' in str(response):
                    # Example Response - {'jsonrpc': '2.0', 'error': {CROPPED}, 'id': 2}
                    nxapi_log.append(YAML_TK['YAML_fqdn'] + ': - [' + str(item) + '] Response Unsuccessful! Reason: "' + str(getset_payload[item]['params']['cmd']) + '" ' + str(response['error']['data']['msg'].strip()))
                    nxapi_status = False

                else:
                    nxapi_log.append(YAML_TK['YAML_fqdn'] + ': - [' + str(item) + '] Response Unhandled ' + str(response))
                    nxapi_status = False


                nxapi_log.append(YAML_TK['YAML_fqdn']+ ': < Config Response: && "' + str(response) + '"')

                # Copy running-config startup-config
                wrmem=[
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

                response = requests.post(
                    myurl,
                    data=json.dumps(wrmem),
                    headers=myheader,
                    auth=(SESSION_TK['ENV_user_un'], SESSION_TK['ENV_user_pw']),
                    verify=False
                ).json()

                # Do not log reponse!!!

                nxapi_status = True

                return nxapi_status, nxapi_log, nxapi_list

            else: # commit Flag not True so report only
                nxapi_log.append(YAML_TK['YAML_fqdn'] + ': > Config Payload: !! "' + str(object) + '"')
                nxapi_status = False
                return nxapi_status, nxapi_log, nxapi_list

        except Exception as e:
            sync_log.append(YAML_TK['YAML_fqdn'] + ': > Config Payload: ERR "' + str(object) + '" < RESULT: FAIL ' + str(e))
            nxapi_status = Flase
            return nxapi_status, nxapi_log, nxapi_list
    else:
        nxapi_log.append(YAML_TK['YAML_fqdn'] + ': NXAPI Mode Invalid')
        nxapi_status = False
        return nxapi_status, nxapi_log, nxapi_list

#!/usr/bin/env python3

# Python3 script with NX-API BOT to get JSON-RPC CLI-ASCII response to payload
# command.
#
# REQUIREMENTS:
# python3 -m pip install -r requirements.txt
#
# NX-API must be enabled on Nexus node!!!:
#  feature nxapi
#  nxapi https port 830
#  nxapi sandbox
#
# USAGE:
# python3 nxapi_command_outputs.py -y {HOST_DNS/IP} -u {USERNAME} -p {PASSWORD}

__author__      = 'Paul Mahan, Francis Crick Institute, London UK'
__copyright__   = 'None. Enjoy :-)'

from argparse import ArgumentParser
import requests
import json

# Import modules from '/modules' sub-folder within script directory.
# Folder name is significant to Python. '__init__.py' file required in Parent and
# sub-folder(s).
from modules._network_borg_xtval import xtval

# URLLIB3 package to diabled SSH warnings
requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning
)

# MAIN
if __name__ == '__main__':

    parser = ArgumentParser(description='Usage:')

    parser.add_argument('-y', '--host', type=str, required=True,
                        help='YAML Group or Hostname')
    parser.add_argument('-u', '--username', type=str, required=True,
                        help='Your TACACS+ Username')
    parser.add_argument('-p', '--password', type=str, required=True,
                        help='Your TACACS+ Password)')

    args = parser.parse_args()

    # GLOBAL COMMAND
    """
    Modify Command As Required!!!
    """
    command = 'show ip route'


    print('\n\n**************')
    print('** JSON-RPC **')
    print('**************')

    # HEADER
    myheader_jsonrpc={'content-type':'application/json-rpc'}

    # PAYLOADS
    payload_jsonrpc_cli=[
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": command,
          "version": 1.2
        },
        "id": 1
      }
    ]

    # URL
    jsonrpc_url = ('https://' + args.host + ':830/ins')

    # RESPONSES
    print('\n\n===== JSON-RPC - CLI RAW RESPONSE =====')
    jsonrpc_cli_response = requests.post(
        jsonrpc_url,
        data=json.dumps(payload_jsonrpc_cli),
        headers=myheader_jsonrpc,
        auth=(args.username, args.password),
        verify=False
    ).json()
    print(json.dumps(jsonrpc_cli_response, indent=4, sort_keys=True))


    print('\n***** JUCY RESPONSE *****')
    rib_type = xtval(jsonrpc_cli_response, 'clientname')
    rib_ifnm = xtval(jsonrpc_cli_response, 'ifname')
    rib_nhop = xtval(jsonrpc_cli_response, 'ipnexthop')
    rib_pfx = xtval(jsonrpc_cli_response, 'ipprefix')
    print(rib_type)
    print(rib_ifnm)
    print(rib_nhop)
    print(rib_pfx)
    print('\n')

    # Use the disct zip function to take 2 lists and merge into a dictionary
    print('\n***** SCHEMA RESPONSE *****')
    schema_list = list(zip(rib_pfx, rib_ifnm, rib_nhop, rib_type))
    print('*****')
    print(schema_list)
    print('*****')
    print(schema_list[0])
    print('*****')
    print(schema_list[1][1])

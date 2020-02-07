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
# python3 nxapi_json-rpc_show-run.py -y {HOST_DNS/IP} -u {USERNAME} -p {PASSWORD}

__author__      = 'Paul Mahan, Francis Crick Institute, London UK'
__copyright__   = 'None. Enjoy :-)'

from argparse import ArgumentParser # Required for CMD Line Arguements
import requests # Required to disable SSH warnings
import json # Required for processing response in JSON

# Import modules from '/modules' sub-folder within script directory.
# Folder name is significant to Python. '__init__.py' file required in Parent and
# sub-folder(s).
from modules._network_borg_nxapi_garbx import garbx # Required to clean NXAPI JSON-RPC CLI-ASCII Response

# URLLIB3 package to diabled SSH warnings
requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning
)

# GLOBAL COMMAND
'''
Modify Command As Required!!!
'''
command = 'show run interface loopback0'

# MAIN
if __name__ == '__main__':

    # CLI Argument Parser
    parser = ArgumentParser(description='Usage:')

    parser.add_argument('-y', '--host', type=str, required=True,
                        help='YAML Group or Hostname')
    parser.add_argument('-u', '--username', type=str, required=True,
                        help='Your TACACS+ Username')
    parser.add_argument('-p', '--password', type=str, required=True,
                        help='Your TACACS+ Password)')

    args = parser.parse_args()

    # HEADER - Global JSON-RPC Header
    myheader_jsonrpc={'content-type':'application/json-rpc'}

    # PAYLOAD - JSON-RPC Payload. Global 'command' variable defined as cmd:
    payload_jsonrpc_ascii=[
      {
        "jsonrpc": "2.0",
        "method": "cli_ascii",
        "params": {
          "cmd": command,
          "version": 1.2
        },
        "id": 1
      }
    ]

    # URL - URL of Network node to be queried.
    jsonrpc_url = ('https://' + args.host + ':830/ins')

    # REQUEST - request to be sent to Newtork Node
    jsonrpc_ascii_response = requests.post(
        jsonrpc_url,
        data=json.dumps(payload_jsonrpc_ascii),
        headers=myheader_jsonrpc,
        auth=(args.username, args.password),
        verify=False
    ).json()

    # RESPONSE sent through NXAPI Garburator.
    stripped_response = garbx(jsonrpc_ascii_response)

    for line in stripped_response:
        print(line)

#!/usr/bin/env python3

# Python3 script with NX-API BOT to get JSON-RPC CLI-ASCII response to payload
# command.
#
# REQUIREMENTS:
# python3 -m pip install nornir. Should cover all the bases.
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

    print('\n\n===== JSON-RPC - CLI-ASCII RAW RESPONSE =====')
    jsonrpc_ascii_response = requests.post(
        jsonrpc_url,
        data=json.dumps(payload_jsonrpc_ascii),
        headers=myheader_jsonrpc,
        auth=(args.username, args.password),
        verify=False
    ).json()
    print(json.dumps(jsonrpc_ascii_response, indent=4, sort_keys=True))


    print('\n\n**************')
    print('**   XML    **')
    print('**************')

    # HEADER
    myheader_xml={'content-type':'application/xml'}

    # PAYLOADS
    payload_xml_cli="""<?xml version="1.0"?>
    <ins_api>
      <version>1.2</version>
      <type>cli_show</type>
      <chunk>0</chunk>
      <sid>sid</sid>
      <input>show ip route</input>
      <output_format>xml</output_format>
    </ins_api>"""

    payload_xml_ascii="""<?xml version="1.0"?>
    <ins_api>
      <version>1.2</version>
      <type>cli_show_ascii</type>
      <chunk>0</chunk>
      <sid>sid</sid>
      <input>show ip route</input>
      <output_format>xml</output_format>
    </ins_api>"""

    payload_xml_conf="""<?xml version="1.0"?>
    <ins_api>
      <version>1.2</version>
      <type>cli_conf</type>
      <chunk>0</chunk>
      <sid>sid</sid>
      <input>show ip route</input>
      <output_format>xml</output_format>
    </ins_api>"""

    # URL
    xml_url = ('https://' + args.host + ':830/ins')

    # REPONSES
    print('\n===== XML - CLI RAW RESPONSE =====')
    xml_cli_response = requests.post(
        xml_url,
        data=payload_xml_cli,
        headers=myheader_xml,
        auth=(args.username, args.password),
        verify=False
    )
    print(xml_cli_response)

    print('\n===== XML - ASCII RAW RESPONSE =====')
    xml_cli_response = requests.post(
        xml_url,
        data=payload_xml_ascii,
        headers=myheader_xml,
        auth=(args.username, args.password),
        verify=False
    )
    print(xml_cli_response)

    print('\n===== XML - CONF RAW RESPONSE =====')
    xml_conf_response = requests.post(
        xml_url,
        data=payload_xml_conf,
        headers=myheader_xml,
        auth=(args.username, args.password),
        verify=False
    )
    print(xml_conf_response)


    print('\n\n**************')
    print('**   JSON   **')
    print('**************')

    # HEADER
    myheader_json = {'content-type':'application/json'}

    # PAYLOADS
    payload_json_cli = {
      "ins_api": {
        "version": "1.2",
        "type": "cli_show",
        "chunk": "0",
        "sid": "1",
        "input": command,
        "output_format": "json"
      }
    }

    payload_json_ascii={
      "ins_api": {
        "version": "1.2",
        "type": "cli_show_ascii",
        "chunk": "0",
        "sid": "1",
        "input": command,
        "output_format": "json"
      }
    }

    payload_json_conf={
      "ins_api": {
        "version": "1.2",
        "type": "cli_conf",
        "chunk": "0",
        "sid": "1",
        "input": command,
        "output_format": "json"
      }
    }

    # URL
    json_url = ('https://' + args.host + ':830/ins')

    # RESPONSES
    print('\n===== JSON - CLI RAW RESPONSE =====')
    json_cli_response = requests.post(
        json_url,
        data=json.dumps(payload_json_cli),
        headers=myheader_json,
        auth=(args.username, args.password),
        verify=False
    ).json()
    print(json.dumps(json_cli_response, indent=4, sort_keys=True))

    print('\n===== JSON - ASCII RAW RESPONSE =====')
    json_ascii_response = requests.post(
        json_url,
        data=json.dumps(payload_json_ascii),
        headers=myheader_json,
        auth=(args.username, args.password),
        verify=False
    ).json()
    print(json.dumps(json_ascii_response, indent=4, sort_keys=True))

    print('\n===== JSON - CONF RAW RESPONSE =====')
    json_conf_response = requests.post(
        json_url,
        data=json.dumps(payload_json_cli),
        headers=myheader_json,
        auth=(args.username, args.password),
        verify=False
    ).json()
    print(json.dumps(json_conf_response, indent=4, sort_keys=True))

#!/usr/bin/env python3

# Python3 script to strip the JSOC-RPC CLI-ASCII response to just the 'msg:' blob.
#
# REQUIREMENTS:
# JSON-RPC CLI-ASCII raw response supported.
#
# RETURNS:
# Stipped response as list []

__author__      = 'Paul Mahan, Francis Crick Institute, London UK'
__copyright__   = 'None. Enjoy :-)'

import re

def garbx(raw_response):

    # [OPTIONAL] Remove comments to view in output.
    # print('\n\n===== JSON-RPC - CLI-ASCII RAW RESPONSE =====')
    # print(json.dumps(jsonrpc_ascii_raw, indent=4, sort_keys=True))


    # Extracts the msg: key value from the JSON request. Shoudl always be THIS
    '''
    {
        "cmd": "show run interface loopback0",
        "id": 1,
        "jsonrpc": "2.0",
        "result": {
            "msg": "THIS..."}
    }
    '''

    filtered_response = raw_response["result"]["msg"]

    # [OPTIONAL] Remove comments to view in output.
    # print('\n\n===== JSON-RPC - CLI-ASCII FILTERED RESPONSE =====')
    # print(filtered_response)

    # [OPTIONAL] Remove comments to view in output.
    # print('\n\n===== JSON-RPC - CLI-ASCII STRIPPED RESPONSE =====')

    x = filtered_response.splitlines()

    # Define list
    stripped_response = []

    for line in x:
        # If line starts with a ! or word version, exclude...
        if line.startswith('!') or line.startswith('version'):
            pass
        # Elif line starts with linebreak, exclude...
        elif re.match(r'^\s*$', line):
            pass
        # Add all other lines to response list
        else:
            stripped_response.append(line.strip())

    return(stripped_response)

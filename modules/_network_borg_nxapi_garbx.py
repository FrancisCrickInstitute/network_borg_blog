'''
Python3 script to strip the JSOC-RPC CLI-ASCII response to just the 'msg:' blob.
'''
#!/usr/bin/env python3

__author__ = 'Paul Mahan, Francis Crick Institute, London UK'
__copyright__ = 'None. Enjoy :-)'

import re

def garbx(raw_response):

    # Extract the msg: key value from the JSON request.
    # {
    #     "cmd": "show run interface loopback0",
    #     "id": 1,
    #     "jsonrpc": "2.0",
    #     "result": {
    #         "msg": "<<< EXTRACT THIS BIT >>>"}
    # }

    filtered_response = raw_response["result"]["msg"]

    # Process "\n" as new lines
    filtered_splitlines = filtered_response.splitlines()

    # Define list
    stripped_response = []

    for line in filtered_splitlines:
        # If line starts with a ! or word version, exclude...
        if line.startswith('!') or line.startswith('version'):
            pass
        # Elif line starts with linebreak, exclude...
        elif re.match(r'^\s*$', line):
            pass
        # Add all other lines to response list
        else:
            stripped_response.append(line.strip())

    return stripped_response

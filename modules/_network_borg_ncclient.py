'''
Python3 script to get and scrape Cisco IOS configuration using NETCONF Client (ncclient)
'''
#!/usr/bin/env python3

__author__ = 'Paul Mahan, Francis Crick Institute, London UK'
__copyright__ = 'None. Enjoy :-)'

from ncclient import manager # Required for NCCLIENT connection
import xmltodict # Required to convert XML toPython DICT {
import pprint # Required to PrettyPrint complex XML, OrderedDict structures
import re # Required for garbx()
import ipdb

def garbx(raw_response):
    '''
    NCCLIENT Garbarator Function. Extracts the <data> key value from the XML response
    '''
    filtered_response = raw_response['rpc-reply']['data']

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

def ncclient(SESSION_TK, YAML_TK, ncclient_mode, item, obj):
    '''
    NetMiko Function
    '''

    ncclient_log = []
    ncclient_list = []
    ncclient_status = False

    # Define Pretty Print format
    pp = pprint.PrettyPrinter(depth=6)

    if SESSION_TK['ARG_debug']: # True
        print('\n**DEBUG (_network_borg_ncclient.py) : Payloads Received:')
        print('SESSION_TK:       ' + str(SESSION_TK))
        print('YAML_TK:          ' + str(YAML_TK))
        print('ITEM:             ' + item)
        print('obj(CMD):         ' + obj)
        print('MODE:             ' + ncclient_mode)

    # Driver Matrix
    # NAPALM Driver 'ios' = NCCLIENT Driver 'cisco_ios'
    # NAPALM Driver 'nxos_ssh' = NCCLIENT Driver 'nexus'
    # Only IOS uses NetMiko so NX-OS is surplus to requirements but retained
    # for future reference,
    if YAML_TK['YAML_driver'] == 'ios':
        driver = 'csr'
        dport = 830
    elif YAML_TK['YAML_driver'] == 'nxos_ssh':
        driver = 'nexus'
        dport = 22

    else:
        ncclient_log.append(YAML_TK['YAML_fqdn'] + ': YAML Driver not supported!')
        return ncclient_status, ncclient_log, ncclient_list

    # If NCCLIENT Mode = GET (i.e. send show command)
    if ncclient_mode == 'get':
        try:

            ipdb.set_trace()

            print(driver)

            # Initialise connection to host with ncclient
            with manager.connect(host=YAML_TK['YAML_fqdn'],
                username=SESSION_TK['ENV_user_un'],
                password=SESSION_TK['ENV_user_pw'],
                port=dport,
                timeout=90,
                hostkey_verify=False,
                device_params={'name': 'csr'}) as m:

                #for capabilities in m.server_capabilities:
                #    print(capabilities)

                # Get the RAW XML response which
                raw_xml = m.exec_command({obj}).xml

                if SESSION_TK['ARG_debug']: # True
                    print('\n**DEBUG (_network_borg_ncclient.py) : RAW XML Response:')
                    pp.pprint(raw_xml)

                # Convert our RAW XML to a RAW Dict {}
                raw_dict = xmltodict.parse(str(raw_xml))

                if SESSION_TK['ARG_debug']: # True
                    print('\n**DEBUG (_network_borg_ncclient.py) : RAW DICT Conversion:')
                    pp.pprint(raw_dict)

                # Parse our RAW DICT through a Garbarator to strip junk
                ncclient_list = garbx(raw_dict)

                if SESSION_TK['ARG_debug']: # True
                    print('\n**DEBUG (_network_borg_ncclient.py) : Filtered List:')
                    print(ncclient_list)

                ncclient_log.append(YAML_TK['YAML_fqdn'] + ': - [' + item + \
                    '] Response "' + obj + '" OK')
                ncclient_status = True

        except Exception as error:
            ncclient_log.append(YAML_TK['YAML_fqdn'] + ': - [' + item + \
            '] Payload "' + obj + '" ERR: ' + str(error))
            ncclient_status = False

    else:
        ncclient_log.append(YAML_TK['YAML_fqdn'] + ': NCCLIENT Mode Not Defined!')

    return ncclient_status, ncclient_log, ncclient_list

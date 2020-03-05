#!/usr/bin/env python3

# Python3 script to get XML response to passed payload.
#
# REQUIREMENTS:
# python3 -m pip install -r requirements.txt
#
# NETCONF-YANG must be enabled on the Cisco node!!!:
#   netconf-yang ssh port 830
#   netconf-yang
#
# USAGE:
# python3 {file}.py -y {YAML_GROUP/HOST}

__author__      = 'Paul Mahan, Francis Crick Institute, London UK'
__copyright__   = 'None. Enjoy :-)'

from argparse import ArgumentParser
from ncclient import manager
import xmltodict
import xml.dom.minidom

from modules._network_borg_xtval import xtval

payload = """
<filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <routing-state xmlns="urn:ietf:params:xml:ns:yang:ietf-routing">
    <routing-instance>
      <ribs>
        <rib/>
      </ribs>
    </routing-instance>
  </routing-state>
</filter>
"""

# MAIN
if __name__ == '__main__':

    parser = ArgumentParser(description='Usage:')

    # script arguments
    parser.add_argument('-y', '--host', type=str, required=True,
                        help='YAML Group or Hostname')
    parser.add_argument('-u', '--username', type=str, required=True,
                        help="Device Username (netconf agent username)")
    parser.add_argument('-p', '--password', type=str, required=True,
                        help="Device Password (netconf agent password)")
    parser.add_argument('--port', type=int, default=830,
                        help="Netconf agent port")
    args = parser.parse_args()

    # connect to netconf agent
    with manager.connect(host=args.host,
                         port=args.port,
                         username=args.username,
                         password=args.password,
                         timeout=90,
                         hostkey_verify=False,
                         device_params={'name': 'csr'}) as m:

        # execute netconf operation
        try:
            raw_xml = m.exec_command(payload).xml
            #data = ET.fromstring(response)
        except:
            pass

        print(raw_xml)

        print ('\n\n##### PRETTY XML #####\n')
        #dict = []
        pretty_xml = xml.dom.minidom.parseString(str(raw_xml)).toprettyxml()
        print(pretty_xml)

        print ('\n\n##### PARSE XML TO DICT #####\n')
        parse_dict = xmltodict.parse(pretty_xml)
        print(parse_dict)

        print('\n\n##### JUCY RESPONSE #####\n')
        # Now I'm just going to pick out the ipnexthop using the xtval module.
        rib_type = xtval(parse_dict, 'source-protocol')
        rib_ifnm = xtval(parse_dict, 'outgoing-interface')
        rib_nhop = xtval(parse_dict, 'next-hop-address')
        rib_pfx = xtval(parse_dict, 'destination-prefix')
        print(rib_type)
        print(rib_ifnm)
        print(rib_nhop)
        print(rib_pfx)
        print('\n')

        # Use the disct zip function to take 2 lists and merge into a dictionary
        print('\n\n##### SCHEMA RESPONSE #####\n')
        schema_list = list(zip(rib_pfx, rib_ifnm, rib_nhop, rib_type))
        print('*****')
        print(schema_list)
        print('*****')
        print(schema_list[0])
        print('*****')
        print(schema_list[1][1])

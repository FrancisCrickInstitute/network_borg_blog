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
# python3 {FILE_NAME}.py -y {HOST_DNS/IP} -u {USERNAME} -p {PASSWORD}

__author__      = 'Paul Mahan, Francis Crick Institute, London UK'
__copyright__   = 'None. Enjoy :-)'

from argparse import ArgumentParser
from ncclient import manager
import json
import xmltodict
import xml.dom.minidom
import xml.etree.ElementTree as ET
from _network_borg_xtval import xtval

# Import modules from '/modules' sub-folder within script directory.
# Folder name is significant to Python. '__init__.py' file required in Parent and
# sub-folder(s).
from modules._network_borg_xtval import xtval

payload = """
<filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <interface>
      <Loopback>
        <name>0</name>
      </Loopback>
    </interface>
  </native>
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
            raw_xml = m.get(payload).xml
            #data = ET.fromstring(response)
        except:
            pass

        print ('\n\n##### PRETTY XML #####\n')
        #dict = []
        pretty_xml = xml.dom.minidom.parseString(str(raw_xml)).toprettyxml()
        print(pretty_xml)

        print ('\n\n##### PARSE XML TO DICT #####\n')
        parse_dict = xmltodict.parse(pretty_xml)
        print(parse_dict)

        print('\n***** JUCY RESPONSE *****')
        # Now I'm just going to pick out the ipnexthop using the xtval module.
        int_num = xtval(parse_dict, '#text')
        int_desc = xtval(parse_dict, 'description')
        int_addr = xtval(parse_dict, 'address')
        int_mask = xtval(parse_dict, 'mask')
        print(int_num)
        print(int_desc)
        print(int_addr)
        print(int_mask)
        print('\n')

        zipped = list(zip(int_num,int_desc,int_addr,int_mask))

        for i in zipped:
            print(i)
            print(i[3])

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
import xmltodict
import xml.dom.minidom

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
            raw_xml = m.exec_command({'show version'})
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

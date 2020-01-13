#!/usr/bin/env python

# Python3 script to render Jinja2 given an item and object

from __future__ import print_function, unicode_literals
import jinja2

__author__      = 'Paul Mahan, Francis Crick Institute, London UK'
__copyright__   = 'None. Enjoy :-)'

# Referenced module function
def j2rdr(YAML_TK, item, object):

    # Initialise Dictionaries
    j2rdr_log = []
    j2rdr_list = []

    file = '../network_j2templates/' + object['TEMPLATE']
    # GET Template Config
    with open(file) as f:
        jinja_template = f.read()

    j = jinja2.Template(jinja_template)

    # These are variable which are sent in the template_set. When
    # the *.j2 file is rendered, if a matching object is defined
    # in the template, it will be replaced. i.e. template_*_snmp.j2
    # has a %VAR0, %VAR1 & VAR2 defined.

    try:
        # Initialise Dict {}
        render_dict = {}

        # The j.render accepts a DICT {}
        # See https://jinja.palletsprojects.com/en/2.10.x/api/ : render([context]) section
        # This function builds the DICT by looping over variables contained in VARS:
        # A DICT Key is created using the "VAR + count" with a value of the sub-object.

        # template_set = {
        #    'SNMP': <<< IS ITEM
        #        [
        #            {
        #            'TEMPLATE': 'template_n7k_dev_snmp.j2', <<< IS OBJECT within OBJECTS
        #            'VARS': <<< IS OBJECT within OBJECTS *** WE ARE HERE ***
        #                [
        #                    {
        #                    'SNMP_LOC': SESSION_TK['YAML_loc'], #YAML Inventory <<< IS SUB-OBJECT
        #                    'SNMP_SRC': 'Loopback0', <<< IS SUB-OBJECT
        #                    'SNMP_KEY': SESSION_TK['ENV_snmp_key'] #System Enviro Var <<< IS SUB-OBJECT
        #                    }
        #                ]
        #            }
        #        ],

        try:

            count = 0 # Zerorise Count

            # For each VAR contained in VARS:
            for var in object['VARS'][0]:
                # Create a DICT item with VAR* as the key
                render_dict['VAR' + str(count)] = str(object['VARS'][0][var])
                count += 1 # Increment count

            # print(str(item) + ' : ' + str(render_dict))
            # If we uncomment the above line, what we get is:
            # SNMP : {'VAR0': 'Building A, Floor X, Room Y, CAB Z', 'VAR1': 'Vlan2900', 'VAR2': '<REMOVED>'}
            # Our *.j2 file is defined to replace VAR* key with its value.
            # e.g. template_c3k_dev_snmp.j2 is defined with multiple fields {{ VAR[0-2] }}
            #   {%- if VAR0 is defined %}
            #   snmp-server location {{ VAR0 }}
            #   {%- endif %}

        except: # Captures ITEMs with no VARS (e.g. AAA). render_dict will be null
            pass

        # Jinja2 render using render_dict {} ...
        jinja_rendered = j.render(render_dict)

        # Use splitlines render line endings (e.g. /n) as actual line endings
        j2rdr_list = jinja_rendered.splitlines()

        # This is to address an oddity? The 1st line in the render is blank?
        j2rdr_list = list(filter(None, j2rdr_list))

        j2rdr_status = True
        j2rdr_log.append(YAML_TK['YAML_fqdn'] + ': - [' + item + '] J2 Render Successful ' + u'\u2714')


    except:
        j2rdr_status = False
        j2rdr_log.append(YAML_TK['YAML_fqdn'] + ': - [' + item + '] J2 Render Unsuccessful ' + u'\u2717')

    return (j2rdr_status, j2rdr_log, j2rdr_list)

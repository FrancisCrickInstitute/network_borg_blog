'''
Python3 script to render Jinja2 given an item and object
'''
#!/usr/bin/env python

from __future__ import print_function, unicode_literals
from jinja2 import FileSystemLoader, StrictUndefined
from jinja2.environment import Environment

__author__ = 'Paul Mahan, Francis Crick Institute, London UK'
__copyright__ = 'None. Enjoy :-)'

def j2rdr(SESSION_TK, YAML_TK, item, obj):
    '''
    J2RDR Function
    '''

    if SESSION_TK['ARG_debug']: # True
        print('\n**DEBUG (_network_borg_j2rdr.py) : [' \
            + item + '] J2RDR Module Variables Recieved:')
        print('OBJECT: ' + str(obj))

    # Initialise Lists
    j2rdr_log = []
    j2rdr_list = []

    try: # Try to render J2 file

        # Our 'obj' will be a dict {} of the template_set (returned in GETSET)
        # with the key value stripped (e.g. SNMP) and the outer-list[]:
        # {'TEMPLATE': 'template_prd_c4ks8_snmp.j2',
        # 'VARS': [{'SNMP_LOC': '<REMOVED>', 'SNMP_SRC': 'Loopback0', 'SNMP_KEY': '<REMOVED'}]}
        #
        # Recall the full template_set looks like:
        # template_set = {
        #    'SNMP':
        #        [
        #            {
        #            'TEMPLATE': 'template_n7k_dev_snmp.j2',
        #            'VARS':
        #                [
        #                    {
        #                    'SNMP_LOC': SESSION_TK['YAML_loc'], #YAML Inventory
        #                    'SNMP_SRC': 'Loopback0',
        #                    'SNMP_KEY': SESSION_TK['ENV_snmp_key'] #System Enviro Var
        #                    }
        #                ]
        #            }
        #        ],

        # Strictly enforce rendering with variables. If variable does not exist
        # bomb out of try: To test, comment our a VAR in the _network_borg_getset.py:
        # template_set. e.g. comment out SNMP_LOC from C4KS8 group will generate
        # a J2 Render error.
        env = Environment(undefined=StrictUndefined)

        # Define location of the j2templates.
        env.loader = FileSystemLoader('../network_j2templates/')

        # Get template using the obj['TEMPLATE'] key value. e.g.
        # template_prd_c4ks8_snmp.j2
        template = env.get_template(obj['TEMPLATE'])

        # If key 'VARS' contained in 'obj', assume we will be rendering the J2
        # template with variables...
        if 'VARS' in obj:
            # Call J2 Render using the Python ** keyword argument.
            # Converts Dict to set of key-value pairs. Google Search
            # on '** keyword arguments' to understand or:
            # https://treyhunner.com/2018/04/keyword-arguments-in-python/

            # VARS returned from the template_set is in a list [] so we need
            # to strip with ['VARS'][0] to a dict {}
            jinja_rendered = template.render(**obj['VARS'][0])

        else:
            # Else, no VARS in 'obj' so just render without. Almost pointless
            # but means we have a consistant *.j2 method for defining a gold
            # -standard config.
            jinja_rendered = template.render()

        # Use splitlines render line endings (e.g. /n) as actual line endings
        j2rdr_list = jinja_rendered.splitlines()

        # Remove None values from list if applicable. See:
        # https://www.geeksforgeeks.org/python-remove-none-values-from-list/
        # Method #3 to understand.
        j2rdr_list = list(filter(None, j2rdr_list))

        if SESSION_TK['ARG_debug'] == True:
            print('\n**DEBUG (_network_borg_j2rdr.py) : [' + item + \
                '] J2 Rendered List:')
            print(j2rdr_list)

        # We've got this far, so assume the J2 Render was successful :-)
        j2rdr_log.append(YAML_TK['YAML_fqdn'] + ': - [' + item + \
            '] J2 Render Successful ')
        j2rdr_status = True

    except Exception as error:
        j2rdr_status = False
        j2rdr_log.append(YAML_TK['YAML_fqdn'] + ': - [' + item + \
            '] J2 Render Error: ' + str(error) + ' required by J2 Render')

    return (j2rdr_status, j2rdr_log, j2rdr_list)

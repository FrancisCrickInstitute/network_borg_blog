'''
Python3 script to render Jinja2 given an item and object
'''
#!/usr/bin/env python

from __future__ import print_function, unicode_literals
import jinja2

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

    # Initialise Dictionaries
    j2rdr_log = []
    j2rdr_list = []

    try: # J2 Template File
        file = '../network_j2templates/' + obj['TEMPLATE']

        # GET Template Config
        with open(file) as file:
            jinja_template = file.read()

        try: # Try to read the file into Jina2
            j = jinja2.Template(jinja_template)
            j2file_status = True

        except Exception as error:
            j2rdr_log.append(YAML_TK['YAML_fqdn'] + ': - [' + item + '] J2 File Error: ' + \
                str(error) + ' * Likely misdefined VAR in ' + str(obj['TEMPLATE']))
            j2file_status = False

        if j2file_status: # True

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

            try: # Parse Variables and add to render_dict

                count = 0 # Zerorise Count

                try: # Define render_dict {} Variables
                    for var in obj['VARS'][0]:
                        # Create a DICT item with VAR* as the key
                        render_dict['VAR' + str(count)] = str(obj['VARS'][0][var])
                        count += 1 # Increment count

                    j2dict_status = True

                except:
                    j2dict_status = False

                finally: # No VARS passed so just leave render_dict {} empty
                    j2dict_status = True

                # print(str(item) + ' : ' + str(render_dict))
                # If we uncomment the above line, what we get is:
                # SNMP : {'VAR0': 'Building A, Floor X, Room Y, CAB Z', 'VAR1': 'Vlan2900', 'VAR2': '<REMOVED>'}
                # Our *.j2 file is defined to replace VAR* key with its value.
                # e.g. template_c3k_dev_snmp.j2 is defined with multiple fields {{ VAR[0-2] }}
                #   {%- if VAR0 is defined %}
                #   snmp-server location {{ VAR0 }}
                #   {%- endif %}

                # Jinja2 render using render_dict {} ...
                if j2dict_status == True:
                    try: # Render J2 File

                        if SESSION_TK['ARG_debug']: # True
                            print('\n**DEBUG (_network_borg_sync.py) : [' + item + \
                                '] J2 Variables Dict:')
                            print(render_dict)

                        jinja_rendered = j.render(render_dict)

                        # Use splitlines render line endings (e.g. /n) as actual line endings
                        j2rdr_list = jinja_rendered.splitlines()

                        # This is to address an oddity? The 1st line in the render is blank?
                        j2rdr_list = list(filter(None, j2rdr_list))

                        if SESSION_TK['ARG_debug'] == True:
                            print('\n**DEBUG (_network_borg_sync.py) : [' + item + \
                                '] J2 Filtered List:')
                            print(j2rdr_list)

                        j2rdr_log.append(YAML_TK['YAML_fqdn'] + ': - [' + item + \
                            '] J2 Render Successful ')
                        j2rdr_status = True

                    except Exception as error:
                        j2rdr_status = False
                        j2rdr_log.append(YAML_TK['YAML_fqdn'] + ': - [' + item + \
                            '] J2 Render Error: ' + str(error))

                else: # j2dict_status == False
                    j2rdr_status = False

            except Exception as error: # Parse Variables Exception
                j2rdr_status = False
                j2rdr_log.append(YAML_TK['YAML_fqdn'] + ': - [' + item + \
                    '] J2 Render Dictionary Error ' + str(error))

        else: # j2file_status == False
            j2rdr_status = False

    except Exception as error:
        j2rdr_status = False
        j2rdr_log.append(YAML_TK['YAML_fqdn'] + ': - [' + item + \
            '] J2 Render Dictionary Error ' + str(error))

    return (j2rdr_status, j2rdr_log, j2rdr_list)

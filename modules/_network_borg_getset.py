'''
Python3 Script to Return a Template and Payload Set for Given Environment & Model
'''
#!/usr/bin/env python

__author__ = 'Paul Mahan, Francis Crick Institute, London UK'
__copyright__ = 'None. Enjoy :-)'

def getset(SESSION_TK, YAML_TK, HOST_TK):
    '''
    GETSET Function
    '''

    # Initialise
    getset_log = []
    template_set = {}
    payload_set = {}
    getset_status = False

    if SESSION_TK['ARG_debug']: # True
        print('\n**DEBUG (_network_borg_getset.py) : GETSET Module Tokens Received:')
        print('HOST_TK = VENDOR: ' + HOST_TK['VENDOR'] + \
        ' VERSION: ' + HOST_TK['VERSION'] + \
        ' MODEL: ' + HOST_TK['MODEL'] + \
        ' GROUP:' + HOST_TK['GROUP'])
        print('SESSION_TK = ' + str(SESSION_TK))
        print('YAML_TK = ' + str(YAML_TK))

    ########################################################################
    ###                            DEVELOPMENT                           ###
    ########################################################################
    if YAML_TK['YAML_env'] == 'Development':

        ########################################################################
        ### N7K Development                                                  ###
        ########################################################################
        if HOST_TK['GROUP'] == 'N7K':
            try:
                # TEMPLATE SET
                template_set = {
                    #'USER': # Use User with caution!!! Don't bite off the hand which feeds you.
                    #    [
                    #        {
                    #            'TEMPLATE': 'template_dev_n7k_user.j2',
                    #            'VARS':
                    #                [
                    #                    {
                    #                        'ENAB_PW': SESSION_TK['ENV_enab_pw_dev']
                    #                    }
                    #                ]
                    #        }
                    #    ],
                    'SNMP':
                        [
                            {
                                'TEMPLATE': 'template_dev_n7k_snmp.j2',
                                'VARS':
                                    [
                                        {
                                            'SNMP_LOC': YAML_TK['YAML_loc'], #YAML Inventory
                                            'SNMP_SRC': 'loopback0',
                                            'SNMP_KEY': SESSION_TK['ENV_snmp_key'] #System Enviro Var
                                        }
                                    ]
                            }
                        ],
                    'NTP':
                        [
                            {
                                'TEMPLATE': 'template_dev_n7k_ntp.j2',
                                'VARS':
                                    [
                                        {
                                            'NTP_KEY': SESSION_TK['ENV_ntp_key'] #System Enviro Var
                                        }
                                    ]
                            }
                        ],
                    'AAA':
                        [
                            {
                                'TEMPLATE': 'template_dev_n7k_aaa.j2',
                            }
                        ]
                    }

                # PAYLOAD SET
                payload_set = {
                    #'USER': # Use USER with caution!!! Don't bite off the hand which feeds you.
                    #    [
                    #        {
                    #        'CMD': 'show run | inc username'
                    #        }
                    #    ],
                    'SNMP':
                        [
                            {
                                'CMD': 'show run snmp'
                            }
                        ],
                    'NTP':
                        [
                            {
                                'CMD': 'show run ntp'
                            }
                        ],
                    'AAA':
                        [
                            {
                                'CMD': 'show run aaa'
                            }
                        ]
                    }

                getset_status = True
                getset_log.append(YAML_TK['YAML_fqdn'] + \
                    ': - Successfully Retrieved Template & Payload Sets')

            except Exception as error:
                getset_log.append(YAML_TK['YAML_fqdn'] + \
                    ': - Template Retrieval Error - ' + str(error))

        ########################################################################
        ### N5K Development                                                  ###
        ########################################################################
        elif HOST_TK['GROUP'] == 'N5K':
            try:
                # TEMPLATE SET
                template_set = {
                    #'USER': # Use USER with caution!!! Don't bite off the hand which feeds you.
                    #    [
                    #        {
                    #            'TEMPLATE': 'template_dev_n5k_user.j2',
                    #            'VARS':
                    #                [
                    #                    {
                    #                         'ENAB_PW': SESSION_TK['ENV_enab_pw_dev'] #System Enviro Var
                    #                    }
                    #                ]
                    #        }
                    #    ],
                    'SNMP':
                        [
                            {
                                'TEMPLATE': 'template_dev_n5k_snmp.j2',
                                'VARS':
                                    [
                                        {
                                            'SNMP_LOC': YAML_TK['YAML_loc'], #YAML Inventory
                                            'SNMP_SRC': 'Vlan254',
                                            'SNMP_KEY': SESSION_TK['ENV_snmp_key'] #System Enviro Var
                                        }
                                    ]
                            }
                        ],
                    'NTP':
                        [
                            {
                                'TEMPLATE': 'template_dev_n5k_ntp.j2',
                                'VARS':
                                    [
                                        {
                                            'NTP_KEY': SESSION_TK['ENV_ntp_key'] #System Enviro Var
                                        }
                                    ]
                            }
                        ],
                    'AAA':
                        [
                            {
                                'TEMPLATE': 'template_dev_n5k_aaa.j2',
                            }
                        ]
                    }

                # PAYLOAD SET
                payload_set = {
                    #'USER': # Use USER with caution!!! on't bite off the hand which feeds you.
                    #    [
                    #        {
                    #        'CMD': 'show run security'
                    #        }
                    #    ],
                    'SNMP':
                        [
                            {
                                'CMD': 'show run snmp'
                            }
                        ],
                    'NTP':
                        [
                            {
                                'CMD': 'show run ntp'
                            }
                        ],
                    'AAA':
                        [
                            {
                                'CMD': 'show run aaa'
                            }
                        ]
                    }

                getset_status = True
                getset_log.append(YAML_TK['YAML_fqdn'] + \
                   ': - Successfully Retrieved Template & Payload Sets')

            except Exception as error:
                getset_log.append(YAML_TK['YAML_fqdn'] + \
                    ': - Template Retrieval Error - ' + str(error))

        ########################################################################
        ### C3K Development                                                  ###
        ########################################################################
        elif HOST_TK['GROUP'] == 'C3K':
            try:
                # TEMPLATE SET
                template_set = {
                    #'USER': # Use USER with caution!!! on't bite off the hand which feeds you.
                    #    [
                    #        {
                    #            'TEMPLATE': 'template_dev_c3k_user.j2',
                    #            'VARS':
                    #                [
                    #                    {
                    #                        'ENAB_PW': SESSION_TK['ENV_enab_pw_dev'] #System Enviro Var
                    #                    }
                    #                ]
                    #        }
                    #    ],
                    'SNMP':
                        [
                            {
                                'TEMPLATE': 'template_dev_c3k_snmp.j2',
                                'VARS':
                                    [
                                        {
                                            'SNMP_LOC': YAML_TK['YAML_loc'], #YAML Inventory
                                            'SNMP_SRC': 'Vlan2900',
                                            'SNMP_KEY': SESSION_TK['ENV_snmp_key'] #System Enviro Var
                                        }
                                    ]
                            }
                        ],
                    'NTP':
                        [
                            {
                                'TEMPLATE': 'template_dev_c3k_ntp.j2',
                                'VARS':
                                    [
                                        {
                                            'NTP_KEY': SESSION_TK['ENV_ntp_key'] #System Enviro Var
                                        }
                                    ]
                            }
                        ],
                    'AAA':
                        [
                            {
                                'TEMPLATE': 'template_dev_c3k_aaa.j2',
                            }
                        ]
                    }

                # PAYLOAD SET
                payload_set = {
                    #'USER': # Use USER with caution!!!
                    #    [
                    #        {
                    #            'CMD': 'show run | inc username'
                    #        }
                    #    ],
                    'SNMP':
                        [
                            {
                                'CMD': 'show run | inc snmp'
                            }
                        ],
                    'NTP':
                        [
                            {
                                'CMD': 'show run | inc ntp'
                            }
                        ],
                    'AAA':
                        [
                            {
                                'CMD': 'show run | inc aaa'
                            }
                        ]
                    }

                getset_status = True
                getset_log.append(YAML_TK['YAML_fqdn'] + \
                    ': - Successfully Retrieved Template & Payload Sets')

            except Exception as error:
                getset_log.append(YAML_TK['YAML_fqdn'] + \
                    ': - Template Retrieval Error - ' + str(error))

        else:
            getset_status = False
            getset_log.append(YAML_TK['YAML_fqdn'] + ': GETSET Group ' + \
                HOST_TK['GROUP'] + ' Not Supported!!!')

    ########################################################################
    ###                            PRODUCTION                            ###
    ########################################################################
    elif YAML_TK['YAML_env'] == 'Production':

        ########################################################################
        ### N7K Production                                                   ###
        ########################################################################
        if HOST_TK['GROUP'] == 'N7K':
            try:
                # TEMPLATE SET
                template_set = {
                    #'USER': # Use User with caution!!! Don't bite off the hand which feeds you.
                    #    [
                    #        {
                    #            'TEMPLATE': 'template_n7k_user.j2',
                    #           'VARS':
                    #                [
                    #                   {
                    #                       'ENAB_PW': SESSION_TK['ENV_enab_pw']
                    #                   }
                    #               ]
                    #        }
                    #    ],
                    'SNMP':
                        [
                            {
                                'TEMPLATE': 'template_prd_n7k_snmp.j2',
                                'VARS':
                                    [
                                        {
                                            'SNMP_LOC': YAML_TK['YAML_loc'], #YAML Inventory
                                            'SNMP_SRC': 'mgmt0',
                                            'SNMP_KEY': SESSION_TK['ENV_snmp_key'] #System Enviro Var
                                            }
                                    ]
                            }
                        ],
                    'NTP':
                        [
                            {
                                'TEMPLATE': 'template_prd_n7k_ntp.j2',
                                'VARS':
                                    [
                                        {
                                            'NTP_KEY': SESSION_TK['ENV_ntp_key'] #System Enviro Var
                                            }
                                    ]
                            }
                        ],
                    'AAA':
                        [
                            {
                                'TEMPLATE': 'template_prd_n7k_aaa.j2',
                            }
                        ]
                    }

                # PAYLOAD SET
                payload_set = {
                    #'USER': # Use USER with caution!!! on't bite off the hand which feeds you.
                    #    [
                    #        {
                    #        'CMD': 'show run | inc username'
                    #        }
                    #    ],
                    'SNMP':
                        [
                            {
                                'CMD': 'show run snmp'
                            }
                        ],
                    'NTP':
                        [
                            {
                                'CMD': 'show run ntp'
                            }
                        ],
                    'AAA':
                        [
                            {
                                'CMD': 'show run aaa'
                            }
                        ]
                    }

                getset_status = True
                getset_log.append(YAML_TK['YAML_fqdn'] + \
                    ': - Successfully Retrieved Template & Payload Sets')

            except Exception as error:
                getset_log.append(YAML_TK['YAML_fqdn'] + \
                    ': - Template Retrieval Error - ' + str(error))

        ########################################################################
        ### N6K (e.g. 5696Q) Production                                      ###
        ########################################################################
        elif HOST_TK['GROUP'] == 'N6K':
            try:
                # TEMPLATE SET
                template_set = {
                    'USER': # Use User with caution!!! Don't bite off the hand which feeds you.
                        [
                            {
                                'TEMPLATE': 'template_prd_n6k_user.j2',
                                'VARS':
                                    [
                                        {
                                            'ENAB_PW': SESSION_TK['ENV_enab_pw_prd']
                                        }
                                    ]
                            }
                        ],
                    'SNMP':
                        [
                            {
                                'TEMPLATE': 'template_prd_n6k_snmp.j2',
                                'VARS':
                                    [
                                        {
                                            'SNMP_LOC': YAML_TK['YAML_loc'], #YAML Inventory
                                            'SNMP_SRC': 'mgmt0',
                                            'SNMP_KEY': SESSION_TK['ENV_snmp_key'] #System Enviro Var
                                        }
                                    ]
                            }
                        ],
                    'NTP':
                        [
                            {
                                'TEMPLATE': 'template_prd_n6k_ntp.j2',
                                'VARS':
                                    [
                                        {
                                            'NTP_KEY': SESSION_TK['ENV_ntp_key'] #System Enviro Var
                                        }
                                    ]
                            }
                        ],
                    'AAA':
                        [
                            {
                                'TEMPLATE': 'template_prd_n6k_aaa.j2',
                            }
                        ]
                    }

                # PAYLOAD SET
                payload_set = {
                    'USER': # Use USER with caution!!! on't bite off the hand which feeds you.
                        [
                            {
                                'CMD': 'show run security'
                            }
                        ],
                    'SNMP':
                        [
                            {
                                'CMD': 'show run snmp'
                            }
                        ],
                    'NTP':
                        [
                            {
                                'CMD': 'show run ntp'
                            }
                        ],
                    'AAA':
                        [
                            {
                                'CMD': 'show run aaa'
                            }
                        ]
                    }

                getset_status = True
                getset_log.append(YAML_TK['YAML_fqdn'] + \
                    ': - Successfully Retrieved Template & Payload Sets')

            except Exception as error:
                getset_log.append(YAML_TK['YAML_fqdn'] + \
                    ': - Template Retrieval Error - ' + str(error))

        ########################################################################
        ### N5K Production                                                   ###
        ########################################################################
        elif HOST_TK['GROUP'] == 'N5K':
            try:
                # TEMPLATE SET
                template_set = {
                    'SNMP':
                        [
                            {
                                'TEMPLATE': 'template_prd_n5k_snmp.j2',
                                'VARS':
                                    [
                                        {
                                            'SNMP_LOC': YAML_TK['YAML_loc'], #YAML Inventory
                                            'SNMP_SRC': 'Vlan254',
                                            'SNMP_KEY': SESSION_TK['ENV_snmp_key'] #System Enviro Var
                                        }
                                    ]
                            }
                        ],
                    'NTP':
                        [
                            {
                                'TEMPLATE': 'template_n5k_ntp.j2',
                                'VARS':
                                    [
                                        {
                                            'NTP_KEY': SESSION_TK['ENV_ntp_key'] #System Enviro Var
                                        }
                                    ]
                            }
                        ],
                    'AAA':
                        [
                            {
                                'TEMPLATE': 'template_prd_n5k_aaa.j2',
                            }
                        ]
                    }

                # PAYLOAD SET
                payload_set = {
                    #'USER': # Use USER with caution!!! on't bite off the hand which feeds you.
                    #    [
                    #        {
                    #        'CMD': 'show run | inc username'
                    #        }
                    #    ],
                    'SNMP':
                        [
                            {
                                'CMD': 'show run snmp'
                            }
                        ],
                    'NTP':
                        [
                            {
                                'CMD': 'show run ntp'
                            }
                        ],
                    'AAA':
                        [
                            {
                                'CMD': 'show run aaa'
                            }
                        ]
                    }

                getset_status = True
                getset_log.append(YAML_TK['YAML_fqdn'] + \
                    ': - Successfully Retrieved Template & Payload Sets')

            except Exception as error:
                getset_log.append(YAML_TK['YAML_fqdn'] + \
                    ': - Template Retrieval Error - ' + str(error))

        ########################################################################
        ### C3K Production                                                   ###
        ########################################################################
        elif HOST_TK['GROUP'] == 'C3K':
            try:
                # TEMPLATE SET
                template_set = {
                    'USER': # Use User with caution!!! Don't bite off the hand which feeds you.
                        [
                            {
                                'TEMPLATE': 'template_prd_c3k_user.j2',
                                'VARS':
                                    [
                                        {
                                            'ENAB_PW': SESSION_TK['ENV_enab_pw_prd']
                                        }
                                    ]
                            }
                        ],
                    'SNMP':
                        [
                            {
                                'TEMPLATE': 'template_prd_c3k_snmp.j2',
                                'VARS':
                                    [
                                        {
                                            'SNMP_LOC': YAML_TK['YAML_loc'], #YAML Inventory
                                            'SNMP_SRC': 'Loopback0',
                                            'SNMP_KEY': SESSION_TK['ENV_snmp_key'] #System Enviro Var
                                        }
                                    ]
                            }
                        ],
                    'NTP':
                        [
                            {
                                'TEMPLATE': 'template_prd_c3k_ntp.j2',
                                'VARS':
                                    [
                                        {
                                            'NTP_KEY': SESSION_TK['ENV_ntp_key'] #System Enviro Var
                                        }
                                    ]
                            }
                        ],
                    'AAA':
                        [
                            {
                                'TEMPLATE': 'template_prd_c3k_aaa.j2',
                            }
                        ]
                    }

                # PAYLOAD SET
                payload_set = {
                    'USER': # Use USER with caution!!! on't bite off the hand which feeds you.
                        [
                            {
                                'CMD': 'show run | inc username'
                            }
                        ],
                    'SNMP':
                        [
                            {
                                'CMD': 'show run | inc snmp'
                            }
                        ],
                    'NTP':
                        [
                            {
                                'CMD': 'show run | inc ntp'
                            }
                        ],
                    'AAA':
                        [
                            {
                                'CMD': 'show run | inc aaa'
                            }
                        ]
                    }

                getset_status = True
                getset_log.append(YAML_TK['YAML_fqdn'] + \
                    ': - Successfully Retrieved Template & Payload Sets')

            except Exception as error:
                getset_log.append(YAML_TK['YAML_fqdn'] + \
                    ': - Template Retrieval Error - ' + str(error))


        ########################################################################
        ### C4KS8 Production                                                 ###
        ########################################################################
        elif HOST_TK['GROUP'] == 'C4KS8':
            try:
                # TEMPLATE SET
                template_set = {
                    'SNMP':
                        [
                            {
                                'TEMPLATE': 'template_prd_c4ks8_snmp.j2',
                                'VARS':
                                    [
                                        {
                                            'SNMP_LOC': YAML_TK['YAML_loc'], #YAML Inventory
                                            'SNMP_SRC': 'Loopback0',
                                            'SNMP_KEY': SESSION_TK['ENV_snmp_key'] #System Enviro Var
                                        }
                                    ]
                            }
                        ],
                    'NTP':
                        [
                            {
                                'TEMPLATE': 'template_prd_c4ks8_ntp.j2',
                                'VARS':
                                    [
                                        {
                                            'NTP_KEY': SESSION_TK['ENV_ntp_key'] #System Enviro Var
                                        }
                                    ]
                            }
                        ],
                    'AAA':
                        [
                            {
                                'TEMPLATE': 'template_prd_c4ks8_aaa.j2',
                            }
                        ]
                    }

                # PAYLOAD SET
                payload_set = {
                    'SNMP':
                        [
                            {
                                'CMD': 'show run | inc snmp'
                            }
                        ],
                    'NTP':
                        [
                            {
                                'CMD': 'show run | inc ntp'
                            }
                        ],
                    'AAA':
                        [
                            {
                                'CMD': 'show run | inc aaa'
                            }
                        ]
                    }

                getset_status = True
                getset_log.append(YAML_TK['YAML_fqdn'] + \
                    ': - Successfully Retrieved Template & Payload Sets')

            except Exception as error:
                getset_log.append(YAML_TK['YAML_fqdn'] + \
                    ': - Template Retrieval Error - ' + str(error))


        ########################################################################
        ### C4KX Production                                                  ###
        ########################################################################
        elif HOST_TK['GROUP'] == 'C4KX':
            try:
                # TEMPLATE SET
                template_set = {
                    'SNMP':
                        [
                            {
                                'TEMPLATE': 'template_prd_c4kx_snmp.j2',
                                'VARS':
                                    [
                                        {
                                            'SNMP_LOC': YAML_TK['YAML_loc'], #YAML Inventory
                                            'SNMP_SRC': 'Loopback0',
                                            'SNMP_KEY': SESSION_TK['ENV_snmp_key'] #System Enviro Var
                                        }
                                    ]
                            }
                        ],
                    'NTP':
                        [
                            {
                                'TEMPLATE': 'template_prd_c4kx_ntp.j2',
                                'VARS':
                                    [
                                        {
                                            'NTP_KEY': SESSION_TK['ENV_ntp_key'] #System Enviro Var
                                        }
                                    ]
                            }
                        ],
                    'AAA':
                        [
                            {
                                'TEMPLATE': 'template_prd_c4kx_aaa.j2',
                            }
                        ]
                    }

                # PAYLOAD SET
                payload_set = {
                    'SNMP':
                        [
                            {
                                'CMD': 'show rum | inc snmp'
                            }
                        ],
                    'NTP':
                        [
                            {
                                'CMD': 'show run | inc ntp'
                            }
                        ],
                    'AAA':
                        [
                            {
                                'CMD': 'show run | inc aaa'
                            }
                        ]
                    }

                getset_status = True
                getset_log.append(YAML_TK['YAML_fqdn'] + \
                    ': - Successfully Retrieved Template & Payload Sets')

            except Exception as error:
                getset_log.append(YAML_TK['YAML_fqdn'] + \
                    ': - Template Retrieval Error - ' + str(error))

        ########################################################################
        ### C6K Production                                                   ###
        ########################################################################
        elif HOST_TK['GROUP'] == 'C6K':
            try:
                # TEMPLATE SET
                template_set = {
                    'SNMP':
                        [
                            {
                                'TEMPLATE': 'template_prd_c6k_snmp.j2',
                                'VARS':
                                    [
                                        {
                                            'SNMP_LOC': YAML_TK['YAML_loc'], # YAML Inventory
                                            'SNMP_SRC': 'Loopback0',
                                            'SNMP_KEY': SESSION_TK['ENV_snmp_key'] # System Enviro Var
                                        }
                                    ]
                            }
                        ],
                    'NTP':
                        [
                            {
                                'TEMPLATE': 'template_prd_c6k_ntp.j2',
                                'VARS':
                                    [
                                        {
                                            'NTP_KEY': SESSION_TK['ENV_ntp_key'] # System Enviro Var
                                        }
                                    ]
                            }
                        ],
                    'AAA':
                        [
                            {
                                'TEMPLATE': 'template_prd_c6k_aaa.j2',
                            }
                        ]
                    }

                # PAYLOAD SET
                payload_set = {
                    'SNMP':
                        [
                            {
                                'CMD': 'show rum | inc snmp'
                            }
                        ],
                    'NTP':
                        [
                            {
                                'CMD': 'show run | inc ntp'
                            }
                        ],
                    'AAA':
                        [
                            {
                                'CMD': 'show run | inc aaa'
                            }
                        ]
                    }

                getset_status = True
                getset_log.append(YAML_TK['YAML_fqdn'] + \
                    ': - Successfully Retrieved Template & Payload Sets')

            except Exception as error:
                getset_log.append(YAML_TK['YAML_fqdn'] + ': - Template Retrieval Error - ' \
                    + str(error))

        else:
            getset_status = False
            getset_log.append(YAML_TK['YAML_fqdn'] + ': GETSET Group ' + \
                HOST_TK['GROUP'] + ' Not Supported!')


    else: # Environment
        getset_status = False
        getset_log.append(YAML_TK['YAML_fqdn'] + ':  GETSET Environment ' + \
            YAML_TK['YAML_env'] + ' Not Supported!')

    return getset_status, getset_log, template_set, payload_set

#!/usr/bin/env python

# Python3 script to return a template set for a given Environment and Group

__author__      = 'Paul Mahan, Francis Crick Institute, London UK'
__copyright__   = 'None. Enjoy :-)'

def getset(SESSION_TK, YAML_TK, discvry_dict):

    # Initialise
    getset_log = []
    template_set = {}
    payload_set = {}
    getset_status = False

    if SESSION_TK['ARG_debug'] == True:
        print('\n**DEBUG (_network_borg_getset.py) : Dictionaries Received:')
        print('DISCVRY_DICT = VENDOR:' + discvry_dict['VENDOR'] + ' VERSION:' + discvry_dict['VERSION'] + ' MODEL:' + discvry_dict['MODEL'] + ' GROUP:' + discvry_dict['GROUP'])
        print('SESSION_TK = ' + str(SESSION_TK))
        print('YAML_TK = ' + str(YAML_TK))

    getset_log.append(YAML_TK['YAML_fqdn'] + ': GETSET RETRIEVAL STARTED...')

    if YAML_TK['YAML_env'] == 'Development':

        # N7K Development
        if discvry_dict['GROUP'] == 'N7K':
            try:
                # TEMPLATE SET
                template_set = {
                    #'USER': # Use User with caution!!! Don't bite off the hand which feeds you.
                    #    [
                    #        {
                    #        'TEMPLATE': 'template_n7k_dev_user.j2',
                    #        'VARS':
                    #            [
                    #                {
                    #                'ENAB_PW': SESSION_TK['ENV_enab_pw_dev']
                    #                }
                    #            ]
                    #        }
                    #    ],
                    'SNMP':
                        [
                            {
                            'TEMPLATE': 'template_n7k_dev_snmp.j2',
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
                            'TEMPLATE': 'template_n7k_dev_ntp.j2',
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
                            'TEMPLATE': 'template_n7k_dev_aaa.j2',
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
                getset_log.append(YAML_TK['YAML_fqdn'] + ': - Successfully Retrieved Template & Payload Sets ' + u'\u2714')

            except Exception as e:
                getset_log.append(YAML_TK['YAML_fqdn'] + ': - Template Retrieval Error - ' + str(e))

        # N5K Development
        elif discvry_dict['GROUP'] == 'N5K':
            try:
                # TEMPLATE SET
                template_set = {
                    #'USER': # Use USER with caution!!! on't bite off the hand which feeds you.
                    #    [
                    #        {
                    #        'TEMPLATE': 'template_n5k_dev_user.j2',
                    #        'VARS':
                    #            [
                    #                {
                    #                'ENAB_PW': SESSION_TK['ENV_enab_pw_dev'] #System Enviro Var
                    #                }
                    #            ]
                    #        }
                    #    ],
                    'SNMP':
                        [
                            {
                            'TEMPLATE': 'template_n5k_dev_snmp.j2',
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
                            'TEMPLATE': 'template_n5k_dev_ntp.j2',
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
                            'TEMPLATE': 'template_n5k_dev_aaa.j2',
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
                getset_log.append(YAML_TK['YAML_fqdn'] + ': - Successfully Retrieved Template & Payload Sets ' + u'\u2714')

            except Exception as e:
                getset_log.append(YAML_TK['YAML_fqdn'] + ': - Template Retrieval Error - ' + str(e))

        # C3K Development
        elif discvry_dict['GROUP'] == 'C3K':
            try:
                # TEMPLATE SET
                template_set = {
                    #'USER': # Use USER with caution!!!
                    #    [
                    #        {
                    #        'TEMPLATE': 'template_c3k_dev_user.j2',
                    #        'VARS':
                    #            [
                    #                {
                    #                'ENAB_PW': SESSION_TK['ENV_enab_pw_dev'] #System Enviro Var
                    #                }
                    #            ]
                    #        }
                    #    ],
                    'SNMP':
                        [
                            {
                            'TEMPLATE': 'template_c3k_dev_snmp.j2',
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
                            'TEMPLATE': 'template_c3k_dev_ntp.j2',
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
                            'TEMPLATE': 'template_c3k_dev_aaa.j2',
                            }
                        ]
                    }

                # PAYLOAD SET
                payload_set = {
                    #'USER': # Use USER with caution!!!
                    #    [
                    #        {
                    #        'CMD': 'show run | inc username'
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
                getset_log.append(YAML_TK['YAML_fqdn'] + ': - Successfully Retrieved Template & Payload Sets ' + u'\u2714')

            except Exception as e:
                getset_log.append(YAML_TK['YAML_fqdn'] + ': - Template Retrieval Error - ' + str(e))


        else:
            getset_status = False
            getset_log.append(YAML_TK['YAML_fqdn'] + ': GETSET Group ' + diccovry_dict['GROUP'] + ' Not Supported!!!')

    elif SESSION_TK['ENV'] == 'Production':

                # N7K
                if discvry_dict['GROUP'] == 'N7K':
                    try:
                        # TEMPLATE SET
                        template_set = {
                            'SNMP':
                                [
                                    {
                                    'TEMPLATE': 'template_n7k_snmp.j2',
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
                                    'TEMPLATE': 'template_n7k_ntp.j2',
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
                                    'TEMPLATE': 'template_n7k_aaa.j2',
                                    }
                                ]
                            }

                        # PAYLOAD SET
                        payload_set = {
                            'SNMP':
                                [
                                    {
                                    "jsonrpc": "2.0",
                                    "method": "cli_ascii",
                                    "params": {
                                        "cmd": "show run snmp",
                                        "version": 1.2
                                    },
                                    "id": 2
                                    }
                                ],
                            'NTP':
                                [
                                    {
                                    "jsonrpc": "2.0",
                                    "method": "cli_ascii",
                                    "params": {
                                        "cmd": "show run ntp",
                                        "version": 1.2
                                    },
                                    "id": 2
                                    }
                                ],
                            'AAA':
                                [
                                    {
                                    "jsonrpc": "2.0",
                                    "method": "cli_ascii",
                                    "params": {
                                        "cmd": "show run aaa",
                                        "version": 1.2
                                    },
                                    "id": 3
                                    }
                                ]
                        }

                        #getset_dict = template_set
                        getset_status = True
                        getset_log.append(YAML_TK['YAML_fqdn'] + ': - Successfully Retrieved Template & Payload Sets ' + u'\u2714')

                    except Exception as e:
                        getset_log.append(YAML_TK['YAML_fqdn'] + ': - Template Retrieval Error - ' + str(e))

                # N6K (e.g. 5696Q)
                elif discvry_dict['GROUP'] == 'N6K':
                    try:
                        # TEMPLATE SET
                        template_set = {
                            'SNMP':
                                [
                                    {
                                    'TEMPLATE': 'template_n6k_snmp.j2',
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
                                    'TEMPLATE': 'template_n6k_ntp.j2',
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
                                    'TEMPLATE': 'template_n6k_aaa.j2',
                                    }
                                ]
                            }

                        # PAYLOAD SET
                        payload_set = {
                            'SNMP':
                                [
                                    {
                                    "jsonrpc": "2.0",
                                    "method": "cli_ascii",
                                    "params": {
                                        "cmd": "show run snmp",
                                        "version": 1.2
                                    },
                                    "id": 1
                                    }
                                ],
                            'NTP':
                                [
                                    {
                                    "jsonrpc": "2.0",
                                    "method": "cli_ascii",
                                    "params": {
                                        "cmd": "show run ntp",
                                        "version": 1.2
                                    },
                                    "id": 2
                                    }
                                ],
                            'AAA':
                                [
                                    {
                                    "jsonrpc": "2.0",
                                    "method": "cli_ascii",
                                    "params": {
                                        "cmd": "show run aaa",
                                        "version": 1.2
                                    },
                                    "id": 3
                                    }
                                ]
                            }

                        getset_status = True
                        getset_log.append(YAML_TK['YAML_fqdn'] + ': - Successfully Retrieved Template & Payload Sets ' + u'\u2714')

                    except Exception as e:
                        getset_log.append(YAML_TK['YAML_fqdn'] + ': - Template Retrieval Error - ' + str(e))

                # N5K
                elif discvry_dict['GROUP'] == 'N5K':
                    try:
                        # TEMPLATE SET
                        template_set = {
                            'SNMP':
                                [
                                    {
                                    'TEMPLATE': 'template_n5k_snmp.j2',
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
                                    'TEMPLATE': 'template_n5k_aaa.j2',
                                    }
                                ]
                            }

                        # PAYLOAD SET
                        payload_set = {
                            'SNMP':
                                [
                                    {
                                    "jsonrpc": "2.0",
                                    "method": "cli_ascii",
                                    "params": {
                                        "cmd": "show run snmp",
                                        "version": 1.2
                                    },
                                    "id": 1
                                    }
                                ],
                            'NTP':
                                [
                                    {
                                    "jsonrpc": "2.0",
                                    "method": "cli_ascii",
                                    "params": {
                                        "cmd": "show run ntp",
                                        "version": 1.2
                                    },
                                    "id": 2
                                    }
                                ],
                            'AAA':
                                [
                                    {
                                    "jsonrpc": "2.0",
                                    "method": "cli_ascii",
                                    "params": {
                                        "cmd": "show run aaa",
                                        "version": 1.2
                                    },
                                    "id": 3
                                    }
                                ]
                            }

                        getset_status = True
                        getset_log.append(YAML_TK['YAML_fqdn'] + ': - Successfully Retrieved Template & Payload Sets ' + u'\u2714')

                    except Exception as e:
                        getset_log.append(YAML_TK['YAML_fqdn'] + ': - Template Retrieval Error - ' + str(e))

                # C3K
                elif discvry_dict['GROUP'] == 'C3K':
                    try:
                        # TEMPLATE SET
                        template_set = {
                            'SNMP':
                                [
                                    {
                                    'TEMPLATE': 'template_c3k_snmp.j2',
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
                                    'TEMPLATE': 'template_c3k_ntp.j2',
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
                                    'TEMPLATE': 'template_c3k_aaa.j2',
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
                        getset_log.append(YAML_TK['YAML_fqdn'] + ': - Successfully Retrieved Template & Payload Sets ' + u'\u2714')

                    except Exception as e:
                        getset_log.append(YAML_TK['YAML_fqdn'] + ': - Template Retrieval Error - ' + str(e))


                # C4KS8
                elif discvry_dict['GROUP'] == 'C4KS8':
                    try:
                        # TEMPLATE SET
                        template_set = {
                            'SNMP':
                                [
                                    {
                                    'TEMPLATE': 'template_c4ks8_snmp.j2',
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
                                    'TEMPLATE': 'template_c4ks8_ntp.j2',
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
                                    'TEMPLATE': 'template_c4ks8_aaa.j2',
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
                        getset_log.append(YAML_TK['YAML_fqdn'] + ': - Successfully Retrieved Template & Payload Sets ' + u'\u2714')

                    except Exception as e:
                        getset_log.append(YAML_TK['YAML_fqdn'] + ': - Template Retrieval Error - ' + str(e))


                # C4KX
                elif discvry_dict['GROUP'] == 'C4KX':
                    try:
                        # TEMPLATE SET
                        template_set = {
                            'SNMP':
                                [
                                    {
                                    'TEMPLATE': 'template_c4kx_snmp.j2',
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
                                    'TEMPLATE': 'template_c4kx_ntp.j2',
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
                                    'TEMPLATE': 'template_c4kx_aaa.j2',
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
                        getset_log.append(YAML_TK['YAML_fqdn'] + ': - Successfully Retrieved Template & Payload Sets ' + u'\u2714')

                    except Exception as e:
                        getset_log.append(YAML_TK['YAML_fqdn'] + ': - Template Retrieval Error - ' + str(e))

                # C6K
                elif discvry_dict['GROUP'] == 'C6K':
                    try:
                        # TEMPLATE SET
                        template_set = {
                            'SNMP':
                                [
                                    {
                                    'TEMPLATE': 'template_c6k_snmp.j2',
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
                                    'TEMPLATE': 'template_c6k_ntp.j2',
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
                                    'TEMPLATE': 'template_c6k_aaa.j2',
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
                        getset_log.append(YAML_TK['YAML_fqdn'] + ': - Successfully Retrieved Template & Payload Sets ' + u'\u2714')

                    except Exception as e:
                        getset_log.append(YAML_TK['YAML_fqdn'] + ': - Template Retrieval Error - ' + str(e))

                else:
                    getset_status = False
                    getset_log.append(YAML_TK['YAML_fqdn'] + ': GETSET Group ' + diccovry_dict['GROUP'] + ' Not Supported!!!')


    else:
        getset_status = False
        getset_log.append(YAML_TK['YAML_fqdn'] + ':  GETSET Environment ' + SESSION_TK['ENV'] + ' Not Supported!!!')

    return getset_status, getset_log, template_set, payload_set

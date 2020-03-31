'''
Python3 Script to Discover Network Device Using NAPALM
'''
#!/usr/bin/env python

__author__ = 'Paul Mahan, Francis Crick Institute, London UK'
__copyright__ = 'None. Enjoy :-)'

from napalm import get_network_driver

def discvry(SESSION_TK, YAML_TK):
    '''
    Discovery Function
    '''

    if SESSION_TK['ARG_debug']: # True
        print('\n**DEBUG (_network_borg_discvry.py) : DISCVRY Module Session Token Receved:')
        print('FQDN:             ' + YAML_TK['YAML_fqdn'])
        #print('USERNAME:         ' + SESSION_TK['ENV_user_un'])
        #print('PASSWORD:         ' + SESSION_TK['ENV_user_pw'])
        print('DRIVER:           ' + YAML_TK['YAML_driver'])

    # Initialise Dictionaries
    discvry_log = []
    HOST_TK = {}

    discvry_log.append(YAML_TK['YAML_fqdn'] + ': * NAPALM Discovery Started...')
    discvry_status = False # Unless otherwise overwritten

    # Use NAPALM get_network_driver.
    driver = get_network_driver(YAML_TK['YAML_driver'])

    try:
        # Initiate NAPLAM connection, get facts and close connection
        node = driver(hostname=YAML_TK['YAML_fqdn'], \
            username=SESSION_TK['ENV_user_un'], password=SESSION_TK['ENV_user_pw'])
        node.open()
        host_facts = node.get_facts() # Get Facts
        host_config = node.get_config() # Get Running Config
        node.close()

        # Extract model from facts. No need to Strip
        host_facts_model = host_facts['model']

        # Fork on Model:
        # N77-C7710
        if host_facts_model.find('Nexus7700') != -1:
            try:
                # Build HOST_TK from NAPALM fact,
                HOST_TK['VERSION'] = host_facts['os_version']
                # EXAMPLE RETURN: 8.3(2). No need to strip
                HOST_TK['VENDOR'] = host_facts['vendor']
                HOST_TK['MODEL'] = host_facts['model']
                HOST_TK['GROUP'] = 'N7K'
                HOST_TK['INT'] = host_facts['interface_list']
                HOST_TK['CFG'] = host_config
                # Got this far in the try: statement so everything must be OK
                discvry_status = True
                discvry_log.append(YAML_TK['YAML_fqdn'] + ': - Successfully Discovered')

            except Exception as error:
                discvry_status = False
                discvry_log.append(YAML_TK['YAML_fqdn'] + ': - Discovery Failed! ' + str(error))

            return(discvry_status, discvry_log, HOST_TK)

        # N5K-C5696Q
        elif host_facts_model.find('Nexus 5696') != -1:
            try:
                # Build HOST_TK from NAPALM fact,
                HOST_TK['VERSION'] = host_facts['os_version']
                # EXAMPLE RETURN: 7.3(3)N1(1). No need to strip
                HOST_TK['VENDOR'] = host_facts['vendor']
                HOST_TK['MODEL'] = host_facts['model']
                HOST_TK['GROUP'] = 'N6K'
                HOST_TK['CFG'] = host_config
                # Got this far in the try: statement so everything must be OK
                discvry_status = True
                discvry_log.append(YAML_TK['YAML_fqdn'] + ': - Successfully Discovered')

            except Exception as error:
                discvry_status = False
                discvry_log.append(YAML_TK['YAML_fqdn'] + ': - Discovery Failed! ' + str(error))

            return(discvry_status, discvry_log, HOST_TK)

        # N5K-C5548UP
        elif host_facts_model.find('Nexus5548') != -1:
            try:
                # Build HOST_TK from NAPALM fact,
                HOST_TK['VERSION'] = host_facts['os_version']
                # EXAMPLE RETURN: 5.2(1)N1(9b). No need to strip
                HOST_TK['VENDOR'] = host_facts['vendor']
                HOST_TK['INT'] = host_facts['interface_list']
                HOST_TK['MODEL'] = host_facts['model']
                HOST_TK['GROUP'] = 'N5K'
                HOST_TK['CFG'] = host_config
                # Got this far in the try: statement so everything must be OK
                discvry_status = True
                discvry_log.append(YAML_TK['YAML_fqdn'] + ': - Successfully Discovered')

            except Exception as error:
                discvry_status = False
                discvry_log.append(YAML_TK['YAML_fqdn'] + ': - Discovery Failed! ' + str(error))

            return(discvry_status, discvry_log, HOST_TK)

        # WS-C3850
        elif host_facts_model.find('WS-C3850') != -1:
            try:
                version_string = host_facts['os_version']
                # EXAMPLE RETURN: "IOS-XE Software, Catalyst L3 Switch Software
                # (CAT3K_CAA-UNIVERSALK9-M), Version 03.07.05E RELEASE SOFTWARE (fc1)""
                # Get string between 'Version ' and ' '
                host_facts_ver_major = ((version_string.split('Version '))[1].split('.')[0])
                if host_facts_ver_major == '16':
                    HOST_TK['VERSION'] = ((version_string.split('Version '))[1].split(',')[0])
                elif host_facts_ver_major == '03':
                    HOST_TK['VERSION'] = ((version_string.split('Version '))[1].split(' ')[0])
                else:
                    HOST_TK['VERSION'] = 'UNKNOWN'

                # Build HOST_TK from NAPALM fact,
                HOST_TK['VENDOR'] = host_facts['vendor']
                HOST_TK['MODEL'] = host_facts['model']
                HOST_TK['GROUP'] = 'C3K'
                HOST_TK['INT'] = host_facts['interface_list']
                HOST_TK['CFG'] = host_config
                # Got this far in the try: statement so everything must be OK
                discvry_status = True
                discvry_log.append(YAML_TK['YAML_fqdn'] + ': - Successfully Discovered')

            except Exception as error:
                discvry_status = False
                discvry_log.append(YAML_TK['YAML_fqdn'] + ': - Discovery Failed! ' + str(error))

            return(discvry_status, discvry_log, HOST_TK)

        # WS-C4500X-32
        elif host_facts_model.find('4500X') != -1:
            try:
                version_string = host_facts['os_version']
                # EXAMPLE RETURN: "IOS-XE Software, Catalyst 4500 L3 Switch Software
                # (cat4500e-UNIVERSALK9-M), Version 03.06.07.E RELEASE SOFTWARE (fc3)""
                # Get string between 'Version ' and ' '
                HOST_TK['VERSION'] = ((version_string.split('Version '))[1].split(' ')[0])
                HOST_TK['VENDOR'] = host_facts['vendor']
                HOST_TK['MODEL'] = host_facts['model']
                HOST_TK['GROUP'] = 'C4KX'
                HOST_TK['INT'] = host_facts['interface_list']
                HOST_TK['CFG'] = host_config
                # Got this far in the try: statement so everything must be OK
                discvry_status = True
                discvry_log.append(YAML_TK['YAML_fqdn'] + ': - Successfully Discovered')

            except Exception as error:
                discvry_status = False
                discvry_log.append(YAML_TK['YAML_fqdn'] + ': - Discovery Failed! ' + str(error))

            return(discvry_status, discvry_log, HOST_TK)

        # WS-C4510R+E
        elif host_facts_model.find('4510R') != -1:
            try:
                version_string = host_facts['os_version']
                # EXAMPLE RETURN: "IOS-XE Software, Catalyst 4500 L3 Switch Software
                # (cat4500es8-UNIVERSALK9-M), Version 03.07.03.E RELEASE SOFTWARE (fc3)""
                # Get string between 'Version ' and ' '
                HOST_TK['VERSION'] = ((version_string.split('Version '))[1].split(' ')[0])
                HOST_TK['VENDOR'] = host_facts['vendor']
                HOST_TK['MODEL'] = host_facts['model']
                HOST_TK['GROUP'] = 'C4KS8'
                HOST_TK['INT'] = host_facts['interface_list']
                HOST_TK['CFG'] = host_config
                # Got this far in the try: statement so everything must be OK
                discvry_status = True
                discvry_log.append(YAML_TK['YAML_fqdn'] + ': - Successfully Discovered')

            except Exception as error:
                discvry_status = False
                discvry_log.append(YAML_TK['YAML_fqdn'] + ': - Discovery Failed! ' + str(error))

            return(discvry_status, discvry_log, HOST_TK)

        # C6807-XL
        elif host_facts_model.find('C6807-XL') != -1:
            try:
                version_string = host_facts['os_version']
                # EXAMPLE RETURN: "s2t54 Software (s2t54-ADVENTERPRISEK9_NPE-M),
                # Version 15.1(2)SY4a, RELEASE SOFTWARE (fc1)""
                # Get string between 'Version ' and ' '
                HOST_TK['VERSION'] = ((version_string.split('Version '))[1].split(',')[0])
                HOST_TK['VENDOR'] = host_facts['vendor']
                HOST_TK['MODEL'] = host_facts['model']
                HOST_TK['GROUP'] = 'C6K'
                HOST_TK['INT'] = host_facts['interface_list']
                HOST_TK['CFG'] = host_config
                # Got this far in the try: statement so everything must be OK
                discvry_status = True
                discvry_log.append(YAML_TK['YAML_fqdn'] + ': - Successfully Discovered')

            except Exception as error:
                discvry_status = False
                discvry_log.append(YAML_TK['YAML_fqdn'] + ': - Discovery Failed! ' + str(error))

            return(discvry_status, discvry_log, HOST_TK)

        # CATCH-ALL
        else:
            discvry_log.append(YAML_TK['YAML_fqdn'] + ': Discovery Error! Model Not Supported!')
            discvry_status = False
            return(discvry_status, discvry_log, HOST_TK)

    except Exception as error:
        discvry_log.append(YAML_TK['YAML_fqdn'] + ': Discovery Failed! ' + str(error))
        discvry_status = False
        return(discvry_status, discvry_log, HOST_TK)

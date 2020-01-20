#!/usr/bin/env python

# Python3 script to generate a yaml_dict {} given a YAML Group or
# Host argument

__author__      = 'Paul Mahan, Francis Crick Institute, London UK'
__copyright__   = 'None. Enjoy :-)'

from nornir import InitNornir

def genyml(yaml_arg):

    # Initialise Dictionaries
    yaml_log = []
    yaml_dict = {}

    yaml_log.append('YAML ARGUMENT = ' + yaml_arg + ': YAML DISCOVERY STARTED...')
    yaml_status = False # Unless otherwise overwritten

    # Initialise NorNir
    nr = InitNornir(config_file='config.yaml')

    is_host = False
    is_group = False

    # Query YAML HOST file using yaml_arg. If successful, must be a valid host
    # so add to yaml_dict {}

    try:
        nr.inventory.hosts[yaml_arg]
        is_host = True

        # Get a list of facts from the hosts.yaml for the given host (yaml_arg)

        facts_dict = {} # Zero Dict

        try:
            facts_dict['DRIVER'] = nr.inventory.hosts[yaml_arg]['driver'] # NAPALM Driver
            facts_dict['LOC'] = nr.inventory.hosts[yaml_arg]['loc']
            facts_dict['DOMAIN'] = nr.inventory.hosts[yaml_arg]['domain']
            facts_dict['ENV'] = nr.inventory.hosts[yaml_arg]['env']

            fqdn = str(yaml_arg) + '.' + facts_dict['DOMAIN']

            # Create a yaml_dict {} using the FQDM as the key value and
            # facts_dict as n object
            yaml_dict[fqdn] = facts_dict

            yaml_log.append(fqdn + ': - Valid YAML Host ' + u'\u2714')
            yaml_status = True

        except Exception as e:
            yaml_log.append(str(host) + ': Invalid YAML Host. Missing YAML Vars! ' + str(e))
            yaml_status = False

    except:
        pass # Not a host

    # Query YAML GROUP file using yaml_arg. If successful, must be a valid group
    # so iterate over and add to host_list []
    try:
        for host in nr.inventory.children_of_group(yaml_arg):

            is_group = True

            # Get a list of facts from the hosts.yaml for the given host (yaml_arg)

            facts_dict = {} # Zero Dict

            try:
                facts_dict['DRIVER'] = nr.inventory.hosts[str(host)]['driver'] # NAPALM Driver
                facts_dict['LOC'] = nr.inventory.hosts[str(host)]['loc']
                facts_dict['DOMAIN'] = nr.inventory.hosts[str(host)]['domain']
                facts_dict['ENV'] = nr.inventory.hosts[str(host)]['env']

                #Concatenate hostname and domain suffix
                fqdn = str(host) + '.' + facts_dict['DOMAIN']

                # Create a yaml_dict {} using the FQDM as the key value and
                # facts_dict as n object
                yaml_dict[fqdn] = facts_dict

                yaml_log.append(str(fqdn) + ': - Valid YAML Host ' + u'\u2714')
                yaml_status = True

            except Exception as e: # try: unsuccessful
                yaml_log.append(str(host) + ': Invalid YAML Host. Missing YAML Vars! ' + str(e))
                yaml_status = False

    except:
       pass # Not a group

    # If neither HOST or GROUP
    if is_group == False and is_host == False:
        yaml_log.append('ERROR: ' + yaml_arg + ' is neither a valid YAML Group or Hostname!\n')
        yaml_status = False

    # If yaml_status == False, YAML Dicovery Error
    if yaml_status == False:
        yaml_log.append('ERROR: YAML Discovery Error!')

    return yaml_status, yaml_log, yaml_dict

#!/usr/bin/env python3
#
# Python3 Network Borg (Resistance is futile)
#
# REQUIREMENTS:
# python3 -m pip install nornir. Should cover all the bases.
#
# USAGE:
# python3 {file}.py -y {YAML_GROUP/HOST}

from argparse import ArgumentParser # Required for Command Line Argument parsing
import datetime # Required for Start/ End time
import sys # Required for Python version check

# Import modules from '/modules' sub-folder within script directory.
# Folder name is significant to Python. '__init__.py' file required in Parent and
# sub-folder(s).
from modules._network_borg_args import args
from modules._network_borg_genyml import genyml

# Detect Python version. Python Major=3, Minor=6 expected
if (sys.version_info < (3, 6)):
     print('Must be running Python 3.6 for Network Borg')
     sys.exit(1)

# Master Log List []
master_log = []

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    RED = '\33[91m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def main():

    # LOG Script Start Date/ Time
    start_time = datetime.datetime.now()
    master_log.append('### START ### : ' + str(start_time) + '\n')


    '''
    CLI ARGUMENTS
    '''

    # Command Line Arguement Parser
    parser = ArgumentParser(description='Usage:')

    # Parse command line arguements. action='store_true' defines an arguement
    # without a value. i.e. if -t exisits args.tech == True
    # Example 1:
    # 'python3 network_borg[v***].py -y {YAML Group} -t -v'
    # Defines a YAML Group with the -t (tech-support) and -v (version check)
    # flags set to true.
    #
    # Example 2:
    # 'python3 network_borg[v***].py -y {YAML Group} -o'
    # Defines a YAML Host with the -o {override} flag set to true. Will prompt
    # for username and password even if Environmental Variables are defined.

    parser.add_argument('-y', '--yaml', type=str, required=True,
                        help='YAML Group or Host')
    parser.add_argument('-u', '--username', type=str,
                        help='Username [OPTIONAL]')
    parser.add_argument('-p', '--password', type=str,
                        help='Password [OPTIONAL]')
    parser.add_argument('-t', '--tech', action='store_true',
                        help='Capture Tech Support [OPTIONAL]')
    parser.add_argument('-f', '--ftp', action='store_true',
                        help='Upload Tech Support to FTP [OPTIONAL]')
    parser.add_argument('-c', '--clear', action='store_true',
                        help='Clear Caches (e.g. ARP) [OPTIONAL]')
    parser.add_argument('-v', '--version', action='store_true',
                        help='Verifies Current OS Version against YAML defined Target OS  Version [OPTIONAL]')
    parser.add_argument('-o', '--override', action='store_true',
                        help='Override Stored Credentials and allow manual input only')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Debug Output [OPTIONAL]')
    parser.add_argument('-commit', '--commit', action='store_true',
                        help='[OPTIONAL] Commits the final config PUSH, otherwise Report ONLY')

    cli_args = parser.parse_args()

    SESSION_TK = args(cli_args)


    '''
    YAML: Get List of Hosts
    '''

    # Generate host_list from -y YAML command line argument
    yaml_status, yaml_log, yaml_dict = genyml(SESSION_TK['ARG_yaml'])

    if SESSION_TK['ARG_debug'] == True:
        print('\n**DEBUG (network_borg.py) : YAML DICT')
        print(yaml_dict)

    # Append all log entries to master_log
    for line in yaml_log:
        master_log.append(line)

    # For yaml_host in YAML Dict, process...
    for yaml_host in yaml_dict.items():

        '''
        YAML: Host
        '''

        # yaml_dict will look something like (structured for understanding)
        # {'BP-L08DC-DEV-DSW-01.thecrick.org':
        #   {'NAPALM DRIVER': 'nxos_ssh',
        #    'LOC': 'Building X, Floor Y, Room Z, CAB A',
        #    'DOMAIN': 'thecrick.org',
        #    'ENV': 'Development'
        #   }
        # }
        # YAML_fqdn is in the root dictionary [0]. All other values are in the
        # nested dictionary [1]

        YAML_TK = {} # Re-initialise YAML_TK for each pass of yaml_host

        # Add values to the YAML_TK (Token)
        YAML_TK['YAML_fqdn'] = yaml_host[0]
        YAML_TK['YAML_driver']  = yaml_host[1]['DRIVER'] # Required by NetMiko
        YAML_TK['YAML_loc']  = yaml_host[1]['LOC']
        YAML_TK['YAML_domain']  = yaml_host[1]['DOMAIN']
        YAML_TK['YAML_env']  = yaml_host[1]['ENV']

        if SESSION_TK['ARG_debug'] == True:
            print('\n**DEBUG (network_borg.py) : ' + YAML_TK['YAML_fqdn'] + ' YAML Results:')
            print('FQDN:             ' + YAML_TK['YAML_fqdn'])
            print('DRIVER:           ' + YAML_TK['YAML_driver'])
            print('LOC:              ' + YAML_TK['YAML_loc'])
            print('DOMAIN:           ' + YAML_TK['YAML_domain'])
            print('ENVIRO:           ' + YAML_TK['YAML_env'])

    # LOG Script End Date/ Time
    end_time = datetime.datetime.now()
    master_log.append('\n### END ### : ' + str(end_time))

    diff_time = end_time - start_time
    master_log.append('\n### ELAPSED ### : ' + str(diff_time))

    # Print master_log
    print(bcolors.RED)
    print(bcolors.BOLD)
    print('*********************************************************************')
    print('**                             RESULTS                             **')
    print('*********************************************************************')
    print(bcolors.ENDC)

    for line in master_log:
        print(line)

    print('\n')

if __name__ == "__main__":
    main()

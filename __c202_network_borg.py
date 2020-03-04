#!/usr/bin/env python3
#
# Python3 Network Borg (Resistance is futile)
#
# REQUIREMENTS:
# python3 -m pip install -r requirements.txt
#
# USAGE:
# python3 {file}.py -y {YAML_GROUP/HOST}

__author__      = 'Paul Mahan, Francis Crick Institute, London UK'
__copyright__   = 'None. Enjoy :-)'

from argparse import ArgumentParser # Required for Command Line Argument parsing
import datetime # Required for Start/ End time
import sys # Required for Python version check
import os # Required for screen formatting & writing master_log to file.

# Import modules from '/modules' sub-folder within script directory.
# Folder name is significant to Python. '__init__.py' file required in Parent and
# sub-folder(s).
from modules._network_borg_args import args
from modules._network_borg_genyml import genyml
from modules.__c202_network_borg_sync import sync

# Detect Python version. Python Major=3, Minor=6 expected
if (sys.version_info < (3, 6)):
     print('Must be running Python 3.6 for Network Borg')
     sys.exit(1)

# Master Log List []
master_log = []

# Colour class. Used to format screen output.
class bcolors:
    CEND      = '\33[0m'
    CBOLD     = '\33[1m'
    CITALIC   = '\33[3m'
    CURL      = '\33[4m'
    CBLINK    = '\33[5m'
    CBLINK2   = '\33[6m'
    CSELECTED = '\33[7m'

    CWHITETXTREDBG = '\033[1;37;41m' # White Text, Red Background
    CWHITETXTBLUDBG = '\033[1;37;44m' # White Text, Blue Background
    CWHITETXTYELLOWBK = '\033[1;37;43m' # White Text, Yellow Background
    CWHITETXTCYANBK = '\033[1;37;46m' # White Text, Yellow Background

# Needed for posting to Slack
#with open("../network_config/server.json", "rt") as server_f:
#    credentials = json.load(server_f)
#OAUTH = credentials["OAUTH_TOKEN_PROD"]
#SLACKCHANNEL = credentials["CHANNEL"]
#POST = credentials["POST"]
#client = slack.WebClient(token=OAUTH)

def main():

    # LOG Script Start Date/ Time
    start_time = datetime.datetime.now()
    master_log.append('\n### START ### : ' + str(start_time) + '\n')

    # Use OS function to centralise output to Terminal
    print(bcolors.CWHITETXTREDBG)
    print('\n' + ('Network Borg Python3 Script Started @ ' + str(start_time)).center(os.get_terminal_size().columns))
    print(bcolors.CEND)

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

    master_log.append('Script Executed By: ' + str(SESSION_TK['ENV_user_un']) + '\n')

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

    print(bcolors.CWHITETXTBLUDBG)
    print('\nYAML Host List:\n')
    for item, object in yaml_dict.items():
        print('- ' + item)
    print(bcolors.CEND)

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
        YAML_TK['YAML_driver']  = yaml_host[1]['DRIVER'] # Required by NAPALM
        YAML_TK['YAML_loc']  = yaml_host[1]['LOC']
        YAML_TK['YAML_domain']  = yaml_host[1]['DOMAIN']
        YAML_TK['YAML_env']  = yaml_host[1]['ENV']

        if SESSION_TK['ARG_debug'] == True:
            print(bcolors.CWHITETXTCYANBK)
            print('\n**DEBUG (network_borg.py) : ' + YAML_TK['YAML_fqdn'] + ' Node Information:')
            print('FQDN:             ' + YAML_TK['YAML_fqdn'])
            print('DRIVER:           ' + YAML_TK['YAML_driver'])
            print('LOC:              ' + YAML_TK['YAML_loc'])
            print('DOMAIN:           ' + YAML_TK['YAML_domain'])
            print('ENVIRO:           ' + YAML_TK['YAML_env'])
            print(bcolors.CEND)

        else:
            print(bcolors.CWHITETXTCYANBK)
            print('\nWorking On ' + YAML_TK['YAML_fqdn'] + '... Please Wait...')
            print(bcolors.CEND)

        '''
        SYNC
        '''

        sync_status, sync_log = sync(SESSION_TK, YAML_TK)

        for line in sync_log:
            master_log.append(line)

    # LOG Script End Date/ Time
    end_time = datetime.datetime.now()
    master_log.append('\n### END ### : ' + str(end_time))

    diff_time = end_time - start_time
    master_log.append('\n### ELAPSED ### : ' + str(diff_time) + '\n')

    # PRINT master_log
    print(bcolors.CWHITETXTREDBG)
    print(bcolors.CBOLD)
    print(' *** RESULTS *** ')
    print(bcolors.CEND)

    for line in master_log:
        print(line)

    # WRITE master_log to file
    # Make a folder in script working directory to store results
    logdir = '../LOGS/network_borg/'

    try:
        os.makedirs(logdir)
    except FileExistsError:
        pass # Folder exisits so nothing to do

    f = open(logdir + str(start_time) + '.log', 'w')
    for line in master_log:
        f.write(line + '\n')
    f.close()

if __name__ == "__main__":
    main()

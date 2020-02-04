'''
Network Borg - Resistance is futile

Requirements:
$ python3 -m pip install -r requirements.txt

Usage:
$ python3 {file}.py -y {YAML_GROUP/HOST}
'''
#!/usr/bin/env python3

__author__ = 'Paul Mahan, Francis Crick Institute, London UK'
__copyright__ = 'None. Enjoy :-)'

from argparse import ArgumentParser # Required for Command Line Argument parsing
import datetime # Required for Start/ End time
import sys # Required for Python version check
import os # Required for writing MASTER_LOG to file.

# Import modules from '/modules' sub-folder within script directory.
# Folder name is significant to Python. '__init__.py' file required in Parent and
# sub-folder(s).
from modules._network_borg_args import args
from modules._network_borg_genyml import genyml
from modules.__c600_network_borg_sync import sync

# Detect Python version. Python Major=3, Minor=6 expected
if sys.version_info < (3, 6):
    print('Must be running Python 3.6 for Network Borg')
    sys.exit(1)

# Master Log List []
MASTER_LOG = []

# Colour class. Used to format screen output.
class PrintColours:
    ''' Colour Print to Terminal '''
    CEND = '\33[0m'
    CBOLD = '\33[1m'
    CITALIC = '\33[3m'
    CURL = '\33[4m'
    CBLINK = '\33[5m'
    CBLINK2 = '\33[6m'
    CSELECTED = '\33[7m'
    CWHITETXTREDBG = '\033[1;37;41m' # White Text, Red Background
    CWHITETXTBLUDBG = '\033[1;37;44m' # White Text, Blue Background
    CWHITETXTYELLOWBG = '\033[1;37;43m' # White Text, Yellow Background
    CWHITETXTCYANBG = '\033[1;37;46m' # White Text, Cyan Background

# Needed for posting to Slack
#with open("../network_config/server.json", "rt") as server_f:
#    credentials = json.load(server_f)
#OAUTH = credentials["OAUTH_TOKEN_PROD"]
#SLACKCHANNEL = credentials["CHANNEL"]
#POST = credentials["POST"]
#client = slack.WebClient(token=OAUTH)

def main():
    ''' MAIN FUNCTION '''

    # LOG Script Start Date/ Time
    start_time = datetime.datetime.now()
    MASTER_LOG.append('\n### START ### : ' + str(start_time) + '\n')

    # Use OS function to centralise output to Terminal
    print(PrintColours.CWHITETXTREDBG)
    print('\n' + ('Network Borg Python3 Script Started @ ' + \
        str(start_time)).center(os.get_terminal_size().columns))
    print(PrintColours.CEND)

    ###
    ### CLI ARGUMENTS
    ###

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

    MASTER_LOG.append('Script Executed By: ' + str(SESSION_TK['ENV_user_un']) + '\n')

    ###
    ### YAML: Get List of Hosts
    ###

    # Generate host_list from -y YAML command line argument
    yaml_status, yaml_log, yaml_dict = genyml(SESSION_TK['ARG_yaml'])

    if SESSION_TK['ARG_debug']:
        print('\n**DEBUG (network_borg.py) : YAML DICT')
        print(yaml_dict)

    if not yaml_status: # False
        MASTER_LOG.append(SESSION_TK['ARG_yaml'] + ': General YAML Failure')

    for line in yaml_log:
        MASTER_LOG.append(line)

    print(PrintColours.CWHITETXTBLUDBG)
    print('\nYAML Host List:\n')
    for yaml_host in yaml_dict.items():
        print('- ' + str(yaml_host[0]))
    print(PrintColours.CEND)

    # For yaml_host in YAML Dict, process...
    for yaml_host in yaml_dict.items():

        ###
        ### YAML: Host
        ###

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
        YAML_TK['YAML_driver'] = yaml_host[1]['DRIVER'] # Required by NAPALM
        YAML_TK['YAML_loc'] = yaml_host[1]['LOC']
        YAML_TK['YAML_domain'] = yaml_host[1]['DOMAIN']
        YAML_TK['YAML_env'] = yaml_host[1]['ENV']

        if SESSION_TK['ARG_debug']:
            print(PrintColours.CWHITETXTCYANBG)
            print('\n**DEBUG (network_borg.py) : ' + YAML_TK['YAML_fqdn'] + ' Node Information:')
            print('FQDN:             ' + YAML_TK['YAML_fqdn'])
            print('DRIVER:           ' + YAML_TK['YAML_driver'])
            print('LOC:              ' + YAML_TK['YAML_loc'])
            print('DOMAIN:           ' + YAML_TK['YAML_domain'])
            print('ENVIRO:           ' + YAML_TK['YAML_env'])
            print(PrintColours.CEND)

        else:
            print(PrintColours.CWHITETXTCYANBG)
            print('\nWorking On ' + YAML_TK['YAML_fqdn'] + '... Please Wait...')
            print(PrintColours.CEND)

        ###
        ### SYNC
        ###

        sync_status, sync_log = sync(SESSION_TK, YAML_TK)

        if not sync_status: # False
            MASTER_LOG.append(YAML_TK['YAML_fqdn'] + ': General Sync Failure')

        for line in sync_log:
            MASTER_LOG.append(line)

    # LOG Script End Date/ Time
    end_time = datetime.datetime.now()
    MASTER_LOG.append('\n### END ### : ' + str(end_time))

    diff_time = end_time - start_time
    MASTER_LOG.append('\n### ELAPSED ### : ' + str(diff_time) + '\n')

    # PRINT MASTER_LOG
    print(PrintColours.CWHITETXTREDBG)
    print('\n' + ('*** RESULTS ***').center(os.get_terminal_size().columns))
    print(PrintColours.CEND)

    for line in MASTER_LOG:
        print(line)

    # WRITE MASTER_LOG to file
    # Make a folder in script working directory to store results
    logdir = '../LOGS/network_borg/'

    try:
        os.makedirs(logdir)
    except FileExistsError:
        pass # Folder exisits so nothing to do

    logfile = open(logdir + str(start_time) + '.log', 'w')
    for line in MASTER_LOG:
        logfile.write(line + '\n')
    logfile.close()

if __name__ == "__main__":
    main()

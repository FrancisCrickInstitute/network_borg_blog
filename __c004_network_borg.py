#!/usr/bin/env python3
#
# Python3 Network Borg
#
# REQUIREMENTS:
# python3 -m pip install -r requirements.txt
#
# USAGE:
# python3 {file}.py -y {YAML_GROUP/HOST}

__author__ = 'Paul Mahan, Francis Crick Institute, London UK'
__copyright__ = 'None. Enjoy :-)'

from argparse import ArgumentParser # Required for Command Line Argument parsing
import datetime # Required for Start/ End time
import sys # Required for Python version check
import os # Required for writing MASTER_LOG to file.

# Detect Python version. Python Major=3, Minor=6 expected
if sys.version_info < (3, 6):
    print('Must be running Python 3.6 for Network Borg')
    sys.exit(1)

# Master Log List []
MASTER_LOG = []

# Colour class. Used to format screen output.
class TerminalColours:
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

def main():
    ''' MAIN FUNCTION '''

    # LOG Script Start Date/ Time
    start_time = datetime.datetime.now()
    MASTER_LOG.append('\n### START ### : ' + str(start_time) + '\n')

    # Use OS function to centralise output to Terminal
    print(TerminalColours.CWHITETXTREDBG)
    print('\n' + ('Network Borg Python3 Script Started @ ' + \
        str(start_time)).center(os.get_terminal_size().columns))
    print(TerminalColours.CEND)

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

    # LOG Script End Date/ Time
    end_time = datetime.datetime.now()
    MASTER_LOG.append('\n### END ### : ' + str(end_time))

    diff_time = end_time - start_time
    MASTER_LOG.append('\n### ELAPSED ### : ' + str(diff_time) + '\n')

    # PRINT MASTER_LOG
    print(TerminalColours.CWHITETXTREDBG)
    print('\n' + ('*** RESULTS ***').center(os.get_terminal_size().columns))
    print(TerminalColours.CEND)

    for line in MASTER_LOG:
        print(line)

if __name__ == "__main__":
    main()

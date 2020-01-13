#!/usr/bin/env python3
#
# Python3 Network Borg (Resistance is futile)
#
# REQUIREMENTS:
# python3 -m pip install nornir. Should cover all the bases.
#
#
# USAGE:
# python3 {file}.py -y {YAML_GROUP/HOST}

from argparse import ArgumentParser # Required for Command Line Argument parsing
import sys # Required to get Python version information
import os # Required to create repo folder and FTP Password
import datetime # Required for Start/ End time
import getpass # Required to prompt for username and password in SYSENV's not found.
import base64 # Required for password obfuscation

# Detect Python version. Python Major=3, Minor=6 expected
if (sys.version_info < (3, 6)):
     print('Must be running Python 3.6 for Network Borg')
     sys.exit(1)

# Master Log List []
master_log = []

def main():

    # LOG Script Start Date/ Time
    start_time = datetime.datetime.now()
    master_log.append('### START ### : ' + str(start_time) + '\n')

    '''
    SESSION TOKEN
    '''

    # Initialise a Session Token Dictionary {}
    SESSION_TK = {}

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

    args = parser.parse_args()

    # Add Arguments to the SESSION_TK (Token)
    SESSION_TK['ARG_yaml'] = args.yaml
    SESSION_TK['ARG_tech'] = args.tech
    SESSION_TK['ARG_ftp'] = args.ftp
    SESSION_TK['ARG_clear'] = args.clear
    SESSION_TK['ARG_version'] = args.version
    SESSION_TK['ARG_debug'] = args.debug
    SESSION_TK['ARG_commit'] = args.commit

    '''
    CREDENTIALS
    '''

    # If Override -o not set, try to get credentials from CLI Arguments -u -p,
    # Envirnmental Variables or finally GetPass. Add to SESSION_TK (Token)
    if args.override == False:

        # Username
        if args.username is not None:
            SESSION_TK['ENV_user_un'] = args.username
        else: #is none
            try:
                SESSION_TK['ENV_user_un'] = os.environ['PY_USER_UN']
            except:
                SESSION_TK['ENV_user_un'] = getpass.getpass('Your Username: ')

        # Password
        if args.password is not None:
            SESSION_TK['ENV_user_pw'] = args.password
        else: #is none
            try:
                SESSION_TK['ENV_user_pw'] = os.environ['PY_USER_PW']
            except:
                SESSION_TK['ENV_user_pw'] = getpass.getpass('Your Password: ')

        # Validation
        if ((SESSION_TK['ENV_user_un'] is None) or (SESSION_TK['ENV_user_pw'] is None)):
            print('ERROR: User Credentials Not Found!!!')
            sys.exit(0)

    else:
        SESSION_TK['ENV_user_un'] = getpass.getpass('Your Username: ')
        SESSION_TK['ENV_user_pw'] = getpass.getpass('Your Password: ')


    '''
    ENVIRONMENTAL VARIABLES
    '''

    # GET ENV variables from SYS Environmental Variables. Must be set manually in
    # user account. On Mac OS 10.13 use 'vi ~/.bash_profile' and add the following:
    # export PY_FTP_PW="<REMOVED>"
    # export PY_FTP_UN="<REMOVED>""
    # export PY_FTP_IP="<REMOVED>"
    # Reload Finder 'killall Finder'
    # Use 'env' to discover what is configured.

    # FTP Environmental Variables. Add to SESSION_TK (Token) if found.
    if SESSION_TK['ARG_tech'] == True and SESSION_TK['ARG_ftp'] == True:
        try:
            SESSION_TK['ENV_ftp_ip'] = os.environ['PY_FTP_IP']
            SESSION_TK['ENV_ftp_un'] = os.environ['PY_FTP_UN']
            SESSION_TK['ENV_ftp_pw'] = os.environ['PY_FTP_PW']

        except:
            print('\nWARNING: Technical Support and FTP Upload Flag set to True')
            print('but required Environmental Variables are missing!!!')
            print('tech-support will be captured to nodes local REPO but not')
            print('uploaded to FTP! See notes in network_borg.py code at line 90')

    else:
        pass

    # SNMP Enviromental Variables. Add to SESSION_TK (Token) if found.
    try:
        SESSION_TK['ENV_snmp_key'] = os.environ['PY_SNMP_KEY']

    except:
        print('\nWARNING: Required SNMP Key Environment Variable is missing')
        print('Script may not work as expected. See notes in network_borg.py')
        print('code at line 90\n')

    # NTP Environmental Variables. Add to SESSION_TK (Token) if found.
    try:
        SESSION_TK['ENV_ntp_key'] = os.environ['PY_NTP_KEY']
        SESSION_TK['ENV_ntp_md5'] = os.environ['PY_NTP_MD5']

    except:
        print('\nWARNING: Required NTP Key Environment Variable is missing')
        print('Script may not work as expected. See notes in network_borg.py')
        print('code at line 90\n')

    # Print Arguments
    if SESSION_TK['ARG_debug'] == True:

        # Obfuscate password prior to priting on screen. I could just print *****
        # but this is a bit of fun :-)
        obfuscated_user_pw = base64.b64encode(SESSION_TK['ENV_user_pw'].encode("utf-8"))

        print('\n______________________________________________________________')
        print('Command Line Arguments:')
        print('YAML Group/ Host: ' + SESSION_TK['ARG_yaml'])
        print('Username:         ' + SESSION_TK['ENV_user_un'])
        print('Password:         ' + str(obfuscated_user_pw))
        print('args.tech:        ' + str(SESSION_TK['ARG_tech']))
        print('args.ftp:         ' + str(SESSION_TK['ARG_ftp']))
        print('args.clear:       ' + str(SESSION_TK['ARG_clear']))
        print('args.version:     ' + str(SESSION_TK['ARG_version']))
        print('args.debug:       ' + str(SESSION_TK['ARG_debug']))
        print('args.commit:      ' + str(SESSION_TK['ARG_commit']))
        print('______________________________________________________________')

    # COMMIT Flag
    if SESSION_TK['ARG_commit'] == True:
        print('\n______________________________________________________________')
        print('COMMIT Flag is TRUE "-commit"!')
        print('Are you sure you want to proceed? Recommended action is you')
        print('run without -commit to validate what would happen first.')
        print('______________________________________________________________')
        input('<ENTER>')

    else:
        print('\nCOMMIT Flag is FALSE: Simulation Mode ONLY. Add "-commit" to commit changes!')

    # Append SESSION_TK to master_log []
    master_log.append(SESSION_TK)

    # LOG Script End Date/ Time
    end_time = datetime.datetime.now()
    master_log.append('\n### END ### : ' + str(end_time))

    diff_time = end_time - start_time
    master_log.append('\n### ELAPSED ### : ' + str(diff_time))

    # Print master_log
    print('\n*********************************************************************')
    print('**                             RESULTS                             **')
    print('*********************************************************************\n')
    for line in master_log:
        print(line)

    print('\n')

if __name__ == "__main__":
    main()

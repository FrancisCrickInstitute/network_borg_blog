#!/usr/bin/env python

# Python3 module to backup configuration to FTP server.

__author__      = 'Paul Mahan, Francis Crick Institute, London UK'
__copyright__   = 'None. Enjoy :-)'

import getpass # Required to prompt for username and password in ARG or SYSENV not found.
import base64 # Required for password obfuscation
import base64 # Required for password obfuscation
import os # Required to get OS Environmental Variables
import sys # Reqquired for y/n prompt

def args(cli_args):

    # Initialise a Session Token Dictionary {}
    SESSION_TK = {}

    # Add Arguments to the SESSION_TK (Token)
    SESSION_TK['ARG_yaml'] = cli_args.yaml
    SESSION_TK['ARG_tech'] = cli_args.tech
    SESSION_TK['ARG_ftp'] = cli_args.ftp
    SESSION_TK['ARG_clear'] = cli_args.clear
    SESSION_TK['ARG_version'] = cli_args.version
    SESSION_TK['ARG_debug'] = cli_args.debug
    SESSION_TK['ARG_commit'] = cli_args.commit

    '''
    CREDENTIALS
    '''

    # If Override -o not set, try to get credentials from CLI Arguments -u -p,
    # Envirnmental Variables or finally GetPass. Add to SESSION_TK (Token)
    if cli_args.override == False:

        # Username
        if cli_args.username is not None:
            SESSION_TK['ENV_user_un'] = cli_args.username
        else: #is none
            try:
                SESSION_TK['ENV_user_un'] = os.environ['PY_USER_UN']
            except:
                SESSION_TK['ENV_user_un'] = getpass.getpass('Your Username: ')

        # Password
        if cli_args.password is not None:
            SESSION_TK['ENV_user_pw'] = cli_args.password
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
            ftp_status = True

        except:
            print('\nWARNING: Technical Support and FTP Upload Flag set to True')
            print('but required Environmental Variables are missing!!!')
            print('tech-support will be captured to nodes local REPO but not')
            print('uploaded to FTP! See notes in network_borg.py code at line 90')
            ftp_status = False
    else:
        ftp_status = False

    # SNMP Enviromental Variables. Add to SESSION_TK (Token) if found.
    try:
        SESSION_TK['ENV_snmp_key'] = os.environ['PY_SNMP_KEY']
        snmp_status = True

    except:
        print('\nWARNING: Required SNMP Key Environment Variable is missing')
        print('Script may not work as expected. See notes in network_borg.py')
        print('code at line 90\n')
        snmp_status = False

    # NTP Environmental Variables. Add to SESSION_TK (Token) if found.
    try:
        SESSION_TK['ENV_ntp_key'] = os.environ['PY_NTP_KEY']
        SESSION_TK['ENV_ntp_md5'] = os.environ['PY_NTP_MD5']
        ntp_status = True

    except:
        print('\nWARNING: Required NTP Key Environment Variable is missing')
        print('Script may not work as expected. See notes in network_borg.py')
        print('code at line 90\n')
        ntp_status = False

    # USER Enviromental Variables. Add to SESSION_TK (Token) if found.
    try:
        SESSION_TK['ENV_enab_pw_prd'] = os.environ['PY_ENAB_PW_PRD']
        SESSION_TK['ENV_enab_pw_dev'] = os.environ['PY_ENAB_PW_DEV']
        enab_status = True

    except:
        print('\nWARNING: Required Enable Password Environment Variable is missing')
        print('Script may not work as expected. See notes in network_borg.py')
        print('code at line 90\n')
        enab_status = False

    # COMMIT Flag
    if SESSION_TK['ARG_commit'] == True:
        print('\n______________________________________________________________')
        print('COMMIT Flag is TRUE "-commit"!')
        print('Are you sure you want to proceed? Recommended action is you')
        print('run without -commit to validate what would happen first.')
        print('______________________________________________________________')
        yes = {'yes','y','ye'} # Accepted Yes values
        no = {'no','n',''} # Accepted No values including CR
        choice = str(input('PROCEED (y/n)? ').lower().strip())
        if choice in yes:
            pass
        elif choice in no:
            sys.exit(0)
        else:
            sys.stdout.write('Pleasse respond with "' + str(yes) + '" or "' + str(no) + '"\n')
            sys.exit(0)

    else:
        print('\nCOMMIT Flag is FALSE: Simulation Mode ONLY. Add "-commit" to commit changes!')


    # Print SESSION_TK (Token)
    if SESSION_TK['ARG_debug'] == True:
        print('\n**DEBUG (network_borg_sync) : SESSION_TK (Token)')
        print('ARG YAML:         ' + SESSION_TK['ARG_yaml'])
        print('ARG Tech:         ' + str(SESSION_TK['ARG_tech']))
        print('ARG FTP:          ' + str(SESSION_TK['ARG_ftp']))
        print('ARG Clear:        ' + str(SESSION_TK['ARG_clear']))
        print('ARG Version       ' + str(SESSION_TK['ARG_version']))
        print('ARG Debug:        ' + str(SESSION_TK['ARG_debug']))
        print('ARG Commit        ' + str(SESSION_TK['ARG_commit']))

        print('ENV Username * :  ' + str(base64.b64encode(SESSION_TK['ENV_user_un'].encode("utf-8"))))
        print('ENV Password * :  ' + str(base64.b64encode(SESSION_TK['ENV_user_pw'].encode("utf-8"))))

        if ftp_status == True:
            print('ENV FTP IP * :    ' + str(base64.b64encode(SESSION_TK['ENV_ftp_ip'].encode("utf-8"))))
            print('ENV FTP User * :  ' + str(base64.b64encode(SESSION_TK['ENV_ftp_un'].encode("utf-8"))))
            print('ENV FTP Passwd * :' + str(base64.b64encode(SESSION_TK['ENV_ftp_pw'].encode("utf-8"))))

        if snmp_status == True:
            print('ENV SNMP Key * :  ' + str(base64.b64encode(SESSION_TK['ENV_snmp_key'].encode("utf-8"))))

        if ntp_status == True:
            print('ENV NTP Key * :   ' + str(base64.b64encode(SESSION_TK['ENV_ntp_key'].encode("utf-8"))))
            print('ENV NTP MD5 * :   ' + str(base64.b64encode(SESSION_TK['ENV_ntp_md5'].encode("utf-8"))))

        if enab_status == True:
            print('ENV Enable Production Password * : ' + str(base64.b64encode(SESSION_TK['ENV_enab_pw_prd'].encode("utf-8"))))
            print('ENV Enable Develkopment Password * : ' + str(base64.b64encode(SESSION_TK['ENV_enab_pw_dev'].encode("utf-8"))))

        print('* = Obfuscated')

    return SESSION_TK

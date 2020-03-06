#!/usr/bin/env python

import os

def main():
    {SNIP}
    if args.override == False:

        # Username
        if args.username is not None:
            ENV_user_un = args.username
        else: #is none
            try:
                ENV_user_un = os.environ['PY_USER_UN']
            except:
                ENV_user_un = getpass.getpass('Your Username: ')

        # Password
        if args.password is not None:
            ENV_user_pw = args.password
        else: #is none
            try:
                ENV_user_pw = os.environ['PY_USER_PW']
            except:
                ENV_user_pw = getpass.getpass('Your Password: ')

        # Validation
        if ((ENV_user_un is None) or (ENV_user_pw is None)):
            print('ERROR: User Credentials Not Found!!!')
            sys.exit(0)

    else:
        ENV_user_un = getpass.getpass('Your Username: ')
        ENV_user_pw = getpass.getpass('Your Password: ')

#!/usr/bin/env python

from argparse import ArgumentParser

def main ():

    #{SNIP}

    parser = ArgumentParser(description='Usage:')

    parser.add_argument('-y', '--yaml', type=str, required=True, help='YAML Group or Host')

    parser.add_argument('-u', '--username', type=str, help='Username [OPTIONAL]')

    parser.add_argument('-p', '--password', type=str, help='Password [OPTIONAL]')

    parser.add_argument('-o', '--override', action='store_true', help='Override Stored Credentials and allow manual input only')

    parser.add_argument('-d', '--debug', action='store_true', help='Debug Output [OPTIONAL]')

    parser.add_argument('-commit', '--commit', action='store_true', help='[OPTIONAL] Commits the final config PUSH, otherwise Report ONLY')

    args = parser.parse_args()

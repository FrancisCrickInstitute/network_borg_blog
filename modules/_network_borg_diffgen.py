#!/usr/bin/env python

# Python3 script to synchronise configuration

from __future__ import print_function, unicode_literals
import jinja2

import logging
import re

# DIFF function. See 'https://www.geeksforgeeks.org/python-set-difference/'
# to understand usage.
def diff(listA, listB):
    return (list(set(listA) - set (listB)))

# Empty List function. See https://www.geeksforgeeks.org/python-check-whether-list-empty-not/
# to understand. If list is empry, return 1, else return 0.
def enquiry(list):
    if not list:
        return 1
    else:
        return 0

# Referenced module function
def diffgen(SESSION_TK, YAML_TK, sync_getcfg_list, sync_j2rdr_list, item):

    diffgen_status = False

    if SESSION_TK['ARG_debug'] == True:
        print('\n**DEBUG (_network_borg_diffgen.py) : DIFFGEN Dictionaries Recieved:')
        print('J2RDR DICT:  ' + str(sync_j2rdr_list))
        print('GETCFG DICT: ' + str(sync_getcfg_list))

    diffgen_log = []
    diffgen_add = []
    diffgen_del = []

    try:
        diffgen_add_status = False
        diffgen_del_status = False

        # Generate a DIFF list [] of lines to be Added
        diffgen_add = diff(sync_j2rdr_list, sync_getcfg_list)

        if enquiry(diffgen_add):
            diffgen_log.append(YAML_TK['YAML_fqdn'] + ': - [' + item + '] + Add False')
        else:
            diffgen_log.append(YAML_TK['YAML_fqdn'] + ': - [' + item + '] + Add True')
            diffgen_add_status = True

        # Generate a DIFF list [] of lines to be Deleted
        diffgen_del = diff(sync_getcfg_list, sync_j2rdr_list)

        if enquiry(diffgen_del):
            diffgen_log.append(YAML_TK['YAML_fqdn'] + ': - [' + item + '] - Delete False')
        else:
            diffgen_log.append(YAML_TK['YAML_fqdn'] + ': - [' + item + '] - Delete True')
            diffgen_del_status = True

        if (diffgen_add_status == True) or (diffgen_del_status == True):
            diffgen_status = True

        else:
            diffgen_log.append(YAML_TK['YAML_fqdn'] + ': - [' + item + '] No Difference Found')
            diffgen_status = True

    except Exception as e:
        diffgen_log.append(YAML_TK['YAML_fqdn'] + ': - [' + item + '] Difference Failure ' + str(e))
        diffgen_status = False

    return (diffgen_status, diffgen_log, diffgen_add, diffgen_del)

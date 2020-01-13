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
def diffgen(SESSION_TK, YAML_TK, response_list, template_list, item):

    diffgen_log = []
    diffgen_add = []
    diffgen_del = []

    try:
        # Generate a DIFF list [] of lines to be Added
        diffgen_add = diff(template_list, response_list)

        if enquiry(diffgen_add):
            diffgen_log.append(YAML_TK['YAML_fqdn'] + ': - [' + item + '] + Add False')
        else:
            diffgen_log.append(YAML_TK['YAML_fqdn'] + ': - [' + item + '] + Add True')

        # Generate a DIFF list [] of lines to be Deleted
        diffgen_del = diff(response_list, template_list)

        if enquiry(diffgen_del):
            diffgen_log.append(YAML_TK['YAML_fqdn'] + ': - [' + item + '] - Delete False')
        else:
            diffgen_log.append(YAML_TK['YAML_fqdn'] + ': - [' + item + '] - Delete True')

        diffgen_status = True

    except Exception as e:
        diffgen_log.append(YAML_TK['YAML_fqdn'] + ': - [' + item + '] Difference Failure ' + e)
        diffgen_status = False

    return (diffgen_status, diffgen_log, diffgen_add, diffgen_del)

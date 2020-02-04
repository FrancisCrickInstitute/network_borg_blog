'''
Python3 Script to Identify Differences Between Lists
'''
#!/usr/bin/env python

__author__ = 'Paul Mahan, Francis Crick Institute, London UK'
__copyright__ = 'None. Enjoy :-)'

def diff(listA, listB):
    '''
    DIFF Function See 'https://www.geeksforgeeks.org/python-set-difference/'
    to understand usage.
    '''
    return list(set(listA) - set(listB))

def enquiry(diffgen):
    '''
    Empty List function. See https://www.geeksforgeeks.org/python-check-whether-list-empty-not/
    to understand. If list is empry, return 1, else return 0 (default).
    '''

    if not diffgen:
        return 1

def diffgen(SESSION_TK, YAML_TK, sync_getcfg_list, sync_j2rdr_list, item):
    '''
    DIFFGEN Function
    '''

    diffgen_status = False

    if SESSION_TK['ARG_debug']: # True
        print('\n**DEBUG (_network_borg_diffgen.py) : [' + item +'] DIFFGEN Lists Recieved:')
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

        if diffgen_add_status or diffgen_del_status: # Either True
            diffgen_status = True

        else:
            diffgen_log.append(YAML_TK['YAML_fqdn'] + ': - [' + item + '] No Difference Found')
            diffgen_status = True

    except Exception as error:
        diffgen_log.append(YAML_TK['YAML_fqdn'] + ': - [' + item + '] Difference Failure ' + \
            str(error))
        diffgen_status = False

    return (diffgen_status, diffgen_log, diffgen_add, diffgen_del)

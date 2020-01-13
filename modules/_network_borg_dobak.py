#!/usr/bin/env python

# Python3 module to backup configuration to FTP server.

__author__      = 'Paul Mahan, Francis Crick Institute, London UK'
__copyright__   = 'None. Enjoy :-)'

import base64 # Required for password obfuscation
import sys # Required for
import datetime # Required for Start/ End time
import ftplib # Required for FTP Upload

def dobak(SESSION_TK, YAML_TK, CFG):

    if SESSION_TK['ARG_debug'] == True:

        try:
            obfuscated_ftp_pw = base64.b64encode(SESSION_TK['ENV_ftp_pw'].encode("utf-8"))

            print('**DEBUG (_network_borg_discvry.py) : DOBAK Module Session Token:\n')
            print('FQDN:             ' + YAML_TK['YAML_fqdn'])
            print('FTP IP:           ' + str(SESSION_TK['ENV_ftp_ip']))
            print('FTP USERNAME:     ' + SESSION_TK['ENV_ftp_un'])
            print('FTP PASSWORD:     ' + str(obfuscated_ftp_pw) + ' (Obfuscated!)')
            print('CONFIG (bytes):   ' + str(sys.getsizeof(CFG)))

        except Exception as e:
            discvry_log.append(YAML_TK['YAML_fqdn'] + ': - Backup Failed! ' + str(e))

    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    f = YAML_TK['YAML_fqdn'] + '_' + now.isoformat()

    session = ftplib.FTP(SESSION_TK['ENV_ftp_ip'],SESSION_TK['ENV_ftp_un'],SESSION_TK['ENV_ftp_pw'])
    file = open(f,'rb')                  # file to send
    session.storbinary(f, f)     # send the file
    file.close()                                    # close file and FTP
    session.quit()

    dumpdir = '../DUMP/' + chs.upper() + '_' + now

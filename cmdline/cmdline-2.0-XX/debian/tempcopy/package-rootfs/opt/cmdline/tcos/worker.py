#!/usr/bin/env python

# standard modules

import os
import sys

# TCOS modules
import pytcos.tcos as tcos
from Crypto.Cipher import DES3
from notification import Notify

class Decrypter(object):
    """docstring for Decrypter"""
    def __init__(self, license_file):
        super(Decrypter, self).__init__()
        self.license_file = license_file

    def __read_values__(self):
        '''decodes the licence file and returns an object
        '''
        MASTERKEY = 'f_-KpBVrAiTwbsVoO3-FVcwkKlo1e9fszb4byNDbDCX7LdCygpRZBL0dt4_yu3Y7'
        des3 = DES3.new(MASTERKEY, DES3.MODE_CFB, iv)
        with open(self.LICENSE_FILE, 'r') as l:
            while True:
                chunk = l.read(chunk_size)
                if len(chunk) == 0:
                    break
                lic_decoded += chunk
        '''todo: deserialize, convert string to obj '''
        return lic

        class Validationtype:
            VALID, EXPIRED, NOT_VALID = range(2)

    def __validate__(self):
        lic = self.__read_values__()
        '''check for valid program type'''
        try:
            lic.get('program_type')

        pass

        def __enforce__(self):

            class Starter:
    def __init__(self, hashed_dn=None):
        self.HASHED_DN = hashed_dn

        l = tcos.Launcher(hashed_dn=self.HASHED_DN)
        cmdline = l.ENTRY.get('Application.Cmdline', '')
        if not cmdline:
            e = "Application.Cmdline value missing(" + \
                str(sys.exc_info()[0]) + ")"
            l.log(2, e)
            sys.exit(65)

        returncode = os.system(cmdline)

        if returncode != 0:
            e = "Return value not zero(" + \
                str(sys.exc_info()[0]) + "): " + \
                "cmdline: " + cmdline + \
                ", returncode: " + str(returncode)
            l.log(2, e)
            sys.exit(66)

#!/usr/bin/env python

# standard modules

import os
import sys

# TCOS modules
from pytcos.license import Validator




class Starter:
    def __init__(self, entry_dict):
        # top secret
        self.masterkey =  b'f_-KpBVrAiTwbsVoO3-FVcwk'
        self.iv = b"\xaf\x009<\x06\x11(\x8e#w*'B\x97Rw"
        self.cmdline = entry_dict.get('Application.Cmdline', '')

        v = Validator(master_key=self.masterkey, iv=self.iv, schema_values=entry_dict)
        v.simple_notify()

        if not self.cmdline:
            e = "Application.Cmdline value missing(" + \
                str(sys.exc_info()[0]) + ")"
            l.log(2, e)
            sys.exit(65)

        returncode = os.system(self.cmdline)

        if returncode != 0:
            e = "Return value not zero(" + \
                str(sys.exc_info()[0]) + "): " + \
                "cmdline: " + self.cmdline + \
                ", returncode: " + str(returncode)
            l.log(2, e)
            sys.exit(66)

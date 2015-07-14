# -*- coding: utf-8 -*-

################################################################################
# openthinclient.org ThinClient suite
#
# Copyright (C) 2004, 2007 levigo holding GmbH. All Rights Reserved.
#
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place - Suite 330, Boston, MA 02111-1307, USA.
###############################################################################

import base64
import commands
# import gconf
import ldap
import ldap.filter
import ldapurl
import os
import re
import sys
import time
import subprocess
import syslog
import types
import urllib
import gtk
from pytcos.tcos import Util as tcos_util

tu = tcos_util()

# Classes
#
class Util(object):
#    def __init__(self):
    def getUserPass(self, useSSO="no", dialogTitle="Login"):
        if useSSO == "yes" and os.getenv('USER') != "tcos":
            username = os.getenv('USER')
            tcostoken = os.getenv('TCOS_TOKEN')
            if username != None and tcostoken != None:
                username = tcos_util.shellQuote(tu, username)
                try:
                    if os.path.isfile('/usr/local/bin/sso-tcos-auth'):
                        auth = os.popen('/usr/local/bin/sso-tcos-auth')
                        password = auth.read()
                        auth.close()
                        if password != '':
                            password = tcos_util.shellQuote(tu, password)
                            return [username, password]
                        else :
                            raise Exception('Password from SSO was empty.')
                except:
                    pass

        dialog = gtk.Dialog(dialogTitle,
                            None,
                            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                            (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                             gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        dialog.set_default_response(gtk.RESPONSE_ACCEPT)
        userbox = gtk.HBox(True)
        user_label = gtk.Label('Username:')
        userbox.pack_start(user_label)
        user_input = gtk.Entry()
        user_input.set_activates_default(True)
        userbox.pack_start(user_input)
        dialog.vbox.pack_start(userbox)
        passbox = gtk.HBox(True)
        pass_label = gtk.Label('Password:')
        passbox.pack_start(pass_label)
        pass_input = gtk.Entry()
        pass_input.set_activates_default(True)
        pass_input.set_visibility(False)
        passbox.pack_start(pass_input)
        dialog.vbox.pack_start(passbox)
        dialog.show_all()
        dialog_response = dialog.run()
        if dialog_response == gtk.RESPONSE_ACCEPT:
            username = tcos_util.shellQuote(tu, user_input.get_text())
            password = tcos_util.shellQuote(tu, pass_input.get_text())
            if username and password:
                dialog.destroy()
                return [username, password]
        else:
            dialog.destroy()
            return None
        dialog.destroy()
        return []

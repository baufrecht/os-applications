#!/usr/bin/env python 

import os

# update glib schema
#os.system('sudo glib-compile-schemas /usr/share/glib-2.0/schemas/')
# update dconf-suttings
os.system('sudo dconf update')

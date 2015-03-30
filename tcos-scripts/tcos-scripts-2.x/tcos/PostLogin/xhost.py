#!/usr/bin/env python
import os
import re
import pytcos.tcos as tcos

l = tcos.Ldap()
s = tcos.System()
d = tcos.Desktop()
u = tcos.Util()

mac = s.getMac()
ldap_url = s.getLdapUrl() 
client_dn = l.getClientDn(mac, ldap_url)
user_dn = l.getUserDn('tcos', ldap_url)
apps_dn_list = l.getAppsDn(client_dn, user_dn, ldap_url)

types = map(lambda a: l.getGroupOfUniqueNamesInfo(a, ldap_url)["schema"], apps_dn_list)

def ldap_to_dict(entry):
  converted_entry = dict()
  # re -> matches the last part of the ldap_entry (is a tuple)
  p = re.compile(r'[a-zA-Z0-9-]*$')
  
  for e in entry.items():
    m = p.search(e[0])
    s = m.start()
    # get the index of the match, thus to get the end of the string in
    # front -> s - 1, we are interested in the part after the '.'
    key = e[0][s:]
    value = e[1]
 
    converted_entry[key] = value
 
  return converted_entry 



if "desktop" in types:
  index = types.index("desktop")
  ENTRY = ldap_to_dict(l.getNismapentry(apps_dn_list[index], ldap_url))
  del ENTRY['version']
else:
  exit() 

list = ENTRY['xhosts'].split()
list = ['xhost']+list
returncode = os.system(' '.join(list))


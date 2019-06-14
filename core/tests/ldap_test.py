import sys
import ldap
import os
import logging


host = os.getenv('CORE_LDAP_ADDRESS')
dn = os.getenv('CORE_LDAP_DN')
password = os.getenv('CORE_LDAP_PASSWORD')

l = ldap.initialize(host)
l.set_option(ldap.OPT_REFERRALS, 0)
l.protocol_version = 3
l.simple_bind_s(dn, password)

base = "dc=lab,dc=fibercorp,dc=com,dc=ar"
scope = ldap.SCOPE_SUBTREE
filter = "(userPrincipalName=agaona@lab.fibercorp.com.ar)"
attrs = ["sAMAccountName"]

r = l.search_s(base, scope, filter, attrs)


logging.debug(r[0][0])
try:
    logging.debug(l.simple_bind_s(r[0][0], 'asdasdasd'))
except ldap.INVALID_CREDENTIALS:
    logging.error("Error")

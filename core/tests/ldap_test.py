import sys
import ldap

host = "ldap://10.120.78.5"
dn = "cn=fc__netauto,ou=OU Aplicaciones,ou=OU Hornos,dc=lab,dc=fibercorp,dc=com,dc=ar"
password = 'F1b3rc0rp!'

l = ldap.initialize(host)
l.set_option(ldap.OPT_REFERRALS, 0)
l.protocol_version = 3
l.simple_bind_s(dn,password)

base = "dc=lab,dc=fibercorp,dc=com,dc=ar"
scope = ldap.SCOPE_SUBTREE
filter = "(userPrincipalName=agaona@lab.fibercorp.com.ar)"
attrs = ["sAMAccountName"]

r = l.search_s(base, scope, filter, attrs)

# print(r[0][1]['sAMAccountName'][0].decode("utf-8"))

print(r[0][0])
try:
	print(l.simple_bind_s(r[0][0],'asdasdasd'))
except ldap.INVALID_CREDENTIALS:
	print("Error")
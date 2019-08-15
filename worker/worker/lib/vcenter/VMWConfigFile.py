#VMWConfigFile.py

"""
Network, VMware, and general settings for deploying a new Linux VM
"""

"""
General settings
"""
deploy_settings = dict()
deploy_settings["dns_servers"]      = ['8.8.8.8','8.8.4.4']
deploy_settings["port"]             = 443

"""
VCenter settings
"""
vc_settings = dict()
vc_settings["vcenter"] = ".I.P.ADDR.ESS"
vc_settings["datacenter"] = "LAB"
vc_settings["user"] = "administrator@vsphere.local"
vc_settings["password"] = "YourPass"




#GetAllVMWTemplates.py

from VMWConfigFile import *
from pyVim import connect
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim, vmodl
import atexit
import os
import ssl
import requests
import argparse
import time


# Disabling urllib3 ssl warnings
requests.packages.urllib3.disable_warnings()
 
# Disabling SSL certificate verification
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
context.verify_mode = ssl.CERT_NONE



def get_vim_objects(content, vim_type):
    '''Get vim objects of a given type.'''
    return [item for item in content.viewManager.CreateContainerView(
        content.rootFolder, [vim_type], recursive=True
    ).view]

def getDVSId(name):

    dvs_list = getAllDVS()
    print(dvs_list)

    for dvs in dvs_list:
        if dvs['name'] == name:
            return dvs['moId']

    return ""

def getAllDVS():

    try:
        si = None
        try:
            
            si = connect.SmartConnect(host=vc_settings["vcenter"],
                                      user=vc_settings["user"],
                                      pwd=vc_settings["password"],
                                      port=443,
                                      sslContext=context)

        except IOError as e:
            pass
            atexit.register(Disconnect, si)


        distributed_vswtiches = []

        content = si.RetrieveContent()
        for dvs in get_vim_objects(content, vim.DistributedVirtualSwitch):
            if not dvs.config == None:
                distributed_vswtiches.append({'name' : dvs.name, 'moId' : dvs._moId})


    except vmodl.MethodFault as e:
        print("Caught vmodl fault: %s" % e.msg)
        return 1

    except Exception as e:
        print("Caught exception: %s" % str(e))
        return 1

    return distributed_vswtiches


print(getAllDVS())
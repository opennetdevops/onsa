VRF_SERVICES = ['cpeless_mpls', 'cpe_mpls', 'vpls']
ALL_SERVICES = ['cpeless_mpls', 'cpe_mpls', 'vpls', 'projects', 'cpeless_irs', 'vcpe_irs', 'cpe_irs']
VPLS_SERVICES = ['vpls']
PROJECT_SERVICES = ['projects']

ServiceTypes = {
    "cpeless_irs": "CpelessIrs",
    "cpe_irs": "CpeIrs",
    "cpeless_mpls": "CpelessMpls",
    "cpe_mpls": "CpeMpls",
    "vcpe_irs": "VcpeIrs",
    "vpls": "Vpls"
}


# HTTP Error Codes
ERR_BAD_REQUEST = 400
ERR_SERVER_INT_ERROR = 500
ERR_NOT_FOUND = 404


# Error codes 
ERR540 = 540
ERR_NO_PUBLICNETWORKS = 541 # No public networks available
ERR_NO_WAN_NET = 542 # No WAN networks available
ERR_NO_MGMT_NET = 543 # No MGMT networks available
ERR544 = 544 # TBD
ERR545 = 545 # TBD
ERR546 = 546 # TBD
ERR547 = 547 # TBD
ERR548 = 548 # TBD
ERR549 = 529 # TBD
ERR520 = 520

# Inventory Error Codes
ERR_NO_ACCESSPORTS = 521 # No free access ports left at specific access node
ERR_NO_VLANS = 522 # No free vlans left at specific access node
ERR_NO_CLIENTPORTS = 523 # No free client ports left at specific client node
ERR_NO_VRFS = 524 # No free VRF lefts
ERR_NO_LOGICALUNITS = 525 # No free logical units left at specific router node
ERR_NO_PORTGROUPS = 526 # No free portgroups left at specific pod
ERR_NO_CUSTOMERLOCATION = 527 # No customer location
ERR_INVALID_LOCATION = 528 # TBD
ERR_NO_ROUTERNODE = 529 # TBD

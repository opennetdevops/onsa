### Inventory constants

# Finite State Machine Codes
BB_CODES = ["bb", "bb_data"]
CPE_CODES = ["cpe", "cpe_data"]
DATA_CODES = ["bb_data", "cpe_data"]
ACTIVATION_CODES = ["bb", "cpe"]

# Services
VRF_SERVICES = ['cpeless_mpls', 'cpe_mpls', 'vpls']
ALL_SERVICES = ['cpeless_mpls', 'cpe_mpls', 'vpls', 'projects', 'cpeless_irs', 'vcpe_irs', 'cpe_irs']
VPLS_SERVICES = ['vpls']


ONSA_OK = 200

# Error codes 54X
ERR540 = 540
ERR_NO_PUBLICNETWORKS = 541 # No public networks available
ERR544 = 542 # No WAN networks available
ERR543 = 543 # No MGMT networks available
ERR544 = 544 # TBD
ERR545 = 545 # TBD
ERR546 = 546 # TBD
ERR547 = 547 # TBD
ERR548 = 548 # TBD
ERR549 = 529 # TBD



### Inventory constants

# Error codes 52X
ERR520 = 520
ERR521 = 521 # No free access ports left at specific access node
ERR522 = 522 # No free vlans left at specific access node
ERR_NO_CLIENTPORTS = 523 # No free client ports left at specific client node
ERR524 = 524 # No free VRF lefts
ERR_NO_LOGICALUNITS = 525 # No free logical units left at specific router node
ERR526 = 526 # No free portgroups left at specific pod
ERR527 = 527 # TBD
ERR528 = 528 # TBD
ERR529 = 529 # TBD


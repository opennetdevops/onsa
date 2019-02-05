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

# HTTP Error Codes
ERR_BAD_REQUEST = 400
ERR_SERVER_INT_ERROR = 500
ERR_NOT_FOUND = 404

#HTTP STANDARD CODES
ONSA_OK = 200
HTTP_201_CREATED = 201
HTTP_200_OK = 200
HTTP_400_BADREQUEST = 400
HTTP_500_INTERNAL_SERVER_ERROR = 500


#IPAM Error codes
ERR_GENERIC_IPAM = 540
ERR_NO_PUBLICNETWORKS = 541 # No public networks available
ERR_NO_WAN = 542 # No WAN networks available
ERR_NO_MGMT = 543 # No MGMT networks available


#Inventory Error codes
ERR_INVALID_ACCESSPORT = 521
ERR_INVALID_VLANTAG = 522
ERR_INVALID_CLIENTPORT = 523 
ERR_INVALID_VRF = 524
ERR_INVALID_LOGICALUNIT = 525
ERR_INVALID_PORTGROUP = 526
ERR_INVALID_CUSTOMERLOCATION = 527
ERR_INVALID_LOCATION = 528
ERR_INVALID_ROUTERNODE = 529
ERR_INVALID_CLIENTNODE = 530
ERR_INVALID_ACCESSNODE = 531
ERR_INVALID_CLIENT = 532
ERR_INVALID_VIRTUALPOD = 533

ERR_GENERIC_ACCESSPORT = 550
ERR_GENERIC_VLANTAG = 551
ERR_GENERIC_CLIENTPORT = 552 
ERR_GENERIC_VRF = 553
ERR_GENERIC_LOGICALUNIT = 554
ERR_GENERIC_PORTGROUP = 555
ERR_GENERIC_CUSTOMERLOCATION = 556
ERR_GENERIC_LOCATION = 557
ERR_GENERIC_ROUTERNODE = 558
ERR_GENERIC_CLIENTNODE = 559
ERR_GENERIC_ACCESSNODE = 560
ERR_GENERIC_CLIENT = 561
ERR_GENERIC_VIRTUALPOD = 562

ERR_NOFREE_ACCESSPORT = 571
ERR_NOFREE_VLANTAG = 572
ERR_NOFREE_CLIENTPORT = 573 
ERR_NOFREE_VRF = 574
ERR_NOFREE_LOGICALUNIT = 575
ERR_NOFREE_PORTGROUP = 576




#Service related error codes
ERR_INVALID_SERVICE = 590
ERR_COULDNT_REPROCESS = 591



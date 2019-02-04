from django.http import JsonResponse
from charles.constants import *
import logging


class Error(Exception):

    exceptionDict = {
        "AccessNodeException":ERR_INVALID_ACCESSNODE,
        "AccessPortException":ERR_INVALID_ACCESSPORT,
        "ClientException":ERR_INVALID_CLIENT,
        "ClientNodeException":ERR_INVALID_CLIENTNODE,
        "ClientPortException":ERR_INVALID_CLIENTPORT,
        "CustomerLocationException":ERR_INVALID_CUSTOMERLOCATION,
        "IPAMException":ERR_GENERIC_IPAM,
        "LocationException":ERR_INVALID_LOCATION,
        "LogicalUnitException":ERR_INVALID_LOGICALUNIT,
        "PortgroupException":ERR_INVALID_PORTGROUP,
        "RouterNodeException":ERR_INVALID_ROUTERNODE,
        "ServiceException":ERR_INVALID_SERVICE,
        "VirtualPodException":ERR_INVALID_VIRTUALPOD,
        "VlanTagException":ERR_INVALID_VLANTAG,
        "VrfException":ERR_INVALID_VRF
    }


    def name(self):
        return str(self.__class__.__name__)

    def handle(self):
        logging.error(self)
        return JsonResponse({"msg": str(self)}, status=exceptionDict[self.name])
from django.http import JsonResponse
from django.views import View
from inventory.models import Vrf
from inventory.constants import *
from inventory.exceptions import *

import json
import logging
import coloredlogs

coloredlogs.install(level='DEBUG')
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


class VrfView(View):
    def get(self, request, vrf_id=None):
        name = request.GET.get('name')
        client = request.GET.get('client')
        used = request.GET.get('used')
        try:
            if vrf_id is not None:
                vrf = Vrf.objects.filter(rt=vrf_id).values()[0]
                return JsonResponse(vrf, safe=False)
        except IndexError:
            msg = "Vrf not found."
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)

        if name is not None:
            vrf = Vrf.objects.filter(name=name).values()[0]
            return JsonResponse(vrf, safe=False)
        elif client is not None:
            vrfs = Vrf.objects.filter(client=client).values()
            return JsonResponse(list(vrfs), safe=False)
        elif used is not None:
            vrfs = Vrf.objects.filter(used=used).values()
            return JsonResponse(list(vrfs), safe=False)
        else:
            vrfs = Vrf.objects.all().values()
            return JsonResponse(list(vrfs), safe=False)


    def put(self, request, vrf_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        try:
            vrf = Vrf.objects.filter(rt=vrf_id)
            my_vrf = vrf.values()[0]
            vrf.update(**data)
            return JsonResponse(vrf.values()[0], safe=False)
        except IndexError:
            msg = "Vrf not found."
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)

    def post(self, request):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        vrf = Vrf.objects.create(**data)
        vrf.save()
        return JsonResponse(vrf.values()[0], safe=False, status=HTTP_201_CREATED)       


    def delete(self, request, vrf_id):
        try:
            vrf = Vrf.objects.filter(rt=vrf_id)
            my_vrf = vrf.values()[0]
            vrf.delete()
            data = {"Message" : "Vrf deleted successfully"}
            return JsonResponse(data, safe=False)
        except IndexError:
            msg = "Vrf not found."
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)        
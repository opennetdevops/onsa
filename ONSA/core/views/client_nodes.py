# from django.core import serializers
# from django.http import JsonResponse
# from django.views import View
# from ..models import Cpe
# import json


# class ClientNodesView(View):

#     def get(self, request, client_node_id=None):
#         if client_node_id is None:
#             s = Cpe.objects.all().values()
#         else:
#             s = Cpe.objects.filter(pk=client_node_id).values()
#         return JsonResponse(list(s), safe=False)

#     def post(self, request):
#         data = json.loads(request.body.decode(encoding='UTF-8'))
#         cpe = Cpe.objects.create(**data)
#         cpe.save()
#         response = {"message" : "Cpe requested"}
#         return JsonResponse(response)

#     def put(self, request, client_node_id):
#         data = json.loads(request.body.decode(encoding='UTF-8'))
#         cpe = Cpe.objects.get(pk=client_node_id)
#         cpe.update(**data)
#         return JsonResponse(data, safe=False)
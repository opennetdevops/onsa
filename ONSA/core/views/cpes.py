# from django.core import serializers
# from django.http import JsonResponse
# from django.views import View
# from ..models import Cpe
# import json


# class CpesView(View):

#     def get(self, request):
#         s = Cpe.objects.all().values() 
#         return JsonResponse(list(s), safe=False)

#     def post(self, request):
#         data = json.loads(request.body.decode(encoding='UTF-8'))
#         cpe = Cpe.objects.create(**data)
#         cpe.save()
#         response = {"message" : "Cpe requested"}
#         return JsonResponse(response)


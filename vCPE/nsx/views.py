import json

from django.shortcuts import render
from django.http import JsonResponse

from .models import *

from .lib.utils.nsx.edge import *

### API ###

def edges(request):

	edge_list = nsx_edge_get_all()

	print(edge_list)

	data = {"edges" : ""}

	return JsonResponse(data)

def edge(request):

	edgeName = request.GET.get('edgeName')
	edgeId = request.GET.get('edgeId')

	if edgeName:
		
		data = {"edgeName" : edgeName}

		response = JsonResponse(data)

	elif edgeId:

		data = {"edgeId" : edgeId}

		response = JsonResponse(data)

	return response

def logicalswitches(request):

	data = {}

	return JsonResponse(data)

def logicalswitch(request):

	lsName = request.GET.get('lsName')
	virtualwireId = request.GET.get('virtualwireId')

	if lsName:
		
		data = {"lsName" : lsName}

		response = JsonResponse(data)

	elif virtualwireId:

		data = {"virtualwireId" : virtualwireId}

		response = JsonResponse(data)

	else:
		data = {"Error" : "Not Found"}

		response = JsonResponse(data)

	return response

def datacenters(request):

	data = {}

	return JsonResponse(data)

def datacenter(request):

	datacenterName = request.GET.get('datacenterName')
	if datacenterName:		
		data = {"datacenterName" : datacenterName}

		response = JsonResponse(data)

	else:
		data = {"Error" : "Not Found"}

		response = JsonResponse(data)

	return response

def transportzones(request):


	data = {}

	return JsonResponse(data)



###########
import json

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from .models import *

from .lib.utils.nsx.edge import *
from .lib.utils.nsx.logicalswitch import *
from .lib.utils.nsx.transportzone import *
from .lib.utils.vcenter.datacenters import *


### API ###

def edges(request):
	if request.method == "GET":
		data = nsx_edge_get_all()
		return JsonResponse(data,json_dumps_params={'indent': 3})
	else:
		return HttpResponse("Method not permited.")

def edge(request):
	if request.method == "GET":
		edgeName = request.GET.get('edgeName')
		edgeId = request.GET.get('edgeId')

		if edgeName:
			data = nsx_edge_get_by_name(edgeName)
			response = JsonResponse(data, json_dumps_params={'indent': 3})

		elif edgeId:
			data = nsx_edge_get_by_id(edgeId)
			response = JsonResponse(data)

		return response

	else:
		return HttpResponse("Method not permited.")

def logicalswitches(request):
	if request.method == "GET":
		data = get_logicalswitches_all()
		return JsonResponse(data, json_dumps_params={'indent': 3})

	elif request.method == "POST":
		return HttpResponse("Method not permited.")

def logicalswitch(request):
	if request.method == "GET":	
		tzone = request.GET.get('tzone')		
		lsName = request.GET.get('lsName')	
		virtualwireId = request.GET.get('virtualwireId')

		if lsName:
			data = get_logicalswitch(lsName, tzone)
			response = JsonResponse(data, json_dumps_params={'indent': 3})

		elif virtualwireId:
			data = {"virtualwireId" : virtualwireId}
			response = JsonResponse(data, json_dumps_params={'indent': 3})

		else:
			response = HttpResponse("Logical switch not found.")

	else:
		response = HttpResponse("Method not permited.")

	return response

def datacenters(request):
	if request.method == "GET":
		data = get_datacenters_all()
		return JsonResponse(data)

	else:
		return HttpResponse("Method not permited.")

	

def datacenter(request):
	if request.method == "GET":
		datacenterName = request.GET.get('datacenterName')
		if datacenterName:
			dcId = get_datacenter_id(datacenterName)		
			data = {"datacenterName" : datacenterName, "datacenterId" : dcId}

			return JsonResponse(data, json_dumps_params={'indent': 3})

	else:
		return HttpResponse("Method not permited.")


def transportzones(request):

	if request.method == "GET":
		data = get_tz_all()
		return JsonResponse(data, json_dumps_params={'indent': 3})

	else:
		return HttpResponse("Method not permited.")


def clients(request):
	if request.method == "GET":
		data = {"clients" : []}
		for client in Client.objects.all():
			data["clients"].append({"client" : client.name})
		return JsonResponse(data, json_dumps_params={'indent': 3})

	elif request.method == "POST":
		data = request.body
		print(data)


def hubs(request):
	if request.method == "GET":
		data = {"hubs" : []}
		for hub in Hub.objects.all():
			data["hubs"].append({"hub" : hub.name,
								 "transport_zone" : hub.transport_zone_name,
								 "cluster-name" : hub.cluster_name,
								 "datastore-id" : hub.datastore_id,
								 "resourcePool-id" : hub.resource_pool_id,
								 "datacenter-id" : hub.datacenter_id,
								 "uplink-ip" : hub.uplink_ip,
								 "uplink-pg" : hub.uplink_pg,
								 "uplink-pg-id" : hub.uplink_pg_id,
								 "rac-ip" : hub.mx_ip,
								 "vxrail-ae-interface" : hub.vxrail_ae_interface})

		return JsonResponse(data, json_dumps_params={'indent': 3})

	elif request.method == "POST":
		return HttpResponse("Method not yet available.")

def privateirsservices(request):
	if request.method == "GET":
		return HttpResponse("Method not yet available.")

	elif request.method == "POST":
		return HttpResponse("Method not yet available.")


def publicirsservices(request):
	if request.method == "GET":
		data = {"publicservices" : []}

		for publicservice in PublicIrsService.objects.all():
			data["publicservices"].append({"client" : publicservice.client.name,
										   "public_network" : publicservice.public_network.ip+"/"+str(publicservice.public_network.prefix),
										   "edge_name" : publicservice.edge_name,
										   "hub" : publicservice.portgroup.hub.name,
										   "sco" : publicservice.sco_port.sco.name,
										   "product-identifier" : publicservice.product_identifier})

		return JsonResponse(data, json_dumps_params={'indent': 3})

	if request.method == "POST":
		return HttpResponse("Method not yet available.")


def ippublicsegments(request):
	if request.method == "GET":
		data = {"ippublicsegments" : []}

		for segment in IpPublicSegment.objects.all():
			data["ippublicsegments"].append({"ip" : segment.ip, "prefix" : str(segment.prefix), "used" : segment.used})

		return JsonResponse(data, json_dumps_params={'indent': 3})

	if request.method == "POST":
		return HttpResponse("Method not yet available.")

def ipwans(request):
	if request.method == "GET":
		data = {"ipwans" : []}

		for ip in IpWan.objects.all():
			data["ipwans"].append({"hub" : ip.hub.name, "ip" : ip.network, "prefix" : str(ip.prefix), "used" : ip.used})

		return JsonResponse(data, json_dumps_params={'indent': 3})

	if request.method == "POST":
		return HttpResponse("Method not yet available.")

def logicalunits(request):
	if request.method == "GET":
		data = {"logicalunits" : []}

		for lu in LogicalUnit.objects.all():
			data["logicalunits"].append({"id" : lu.logical_unit_id, "used" : ip.used})

		return JsonResponse(data, json_dumps_params={'indent': 3})

	if request.method == "POST":
		return HttpResponse("Method not yet available.")

def portgroups(request):
	if request.method == "GET":
		data = {"portgroups" : []}

		for pg in Portgroup.objects.all():
			data["portgroups"].append({"id" : pg.dvportgroup_id,
									   "used" : pg.used,
									   "name" : pg.name,
									   "vlan-id" : pg.vlan_tag,
									   "hub" : pg.hub.name})

		return JsonResponse(data, json_dumps_params={'indent': 3})

	if request.method == "POST":
		return HttpResponse("Method not yet available.")

def scoports(request):
	if request.method == "GET":
		data = {"sco_ports" : []}

		for sco_port in ScoPort.objects.all():
			data["sco_ports"].append({"sco" : sco_port.sco.name,
									  "name" : sco_port.port,
									  "vlan-id" : sco_port.vlan_tag,
									  "description" : sco_port.description,
									  "used" : sco_port.used})

		return JsonResponse(data, json_dumps_params={'indent': 3})

	if request.method == "POST":
		return HttpResponse("Method not yet available.")


def scos(request):
	if request.method == "GET":
		data = {"scos" : []}

		for sco in Sco.objects.all():
			data["scos"].append({"id" : sco.sco_id,
									   "name" : sco.name,
									   "sco_ae_interface" : sco.sco_ae_interface,
									   "sco_outer_vlan" : sco.sco_outer_vlan,
									   "hub" : sco.hub.name})

		return JsonResponse(data, json_dumps_params={'indent': 3})

	if request.method == "POST":
		return HttpResponse("Method not yet available.")






###########
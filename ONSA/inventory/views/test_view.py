import json

from django.shortcuts import render
from django.template import loader
from django.http import JsonResponse, HttpResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated

from ..models import *

# from .lib.utils.nsx.edge import *
# from .lib.utils.nsx.edge_routing import *
# from .lib.utils.nsx.logicalswitch import *
# from .lib.utils.nsx.transportzone import *
# from .lib.utils.vcenter.datacenters import *
# from .lib.utils.vcenter import portgroups as vc_pg
# from .lib.utils.juniper.mx_config import *

from ipaddress import *
from pprint import pprint

@api_view(["GET"])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes((IsAuthenticated,))
def test(request):
    locations = Location.objects.filter(name="CENTRO")
    VlanTag.initialize()
    routerNode = locations[0].get_router_node()
    print(routerNode)
    newAccessNode = AccessNode.add("AN", "1.1.1.1", "TN2020", 7, locations[0])
    pprint(newAccessNode)
    # pprint(newAccessNode.get_access_ports_from_node())
    access_port = newAccessNode.assign_free_access_port_from_node()
    print(access_port)
    print(access_port.get_free_vlans())
    print(access_port.get_used_vlans())
    vlan = access_port.assign_free_vlan()
    print("vlan: ",vlan)
    


    newAccessNode.delete()

    data = "{}"
    return JsonResponse(data)


# def edges(request):
#     data = nsx_edge_get_all()
#     return JsonResponse(data,json_dumps_params={'indent': 3})

# @api_view(["GET"])
# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes((IsAuthenticated,))
# def edge(request):
#     edgeName = request.GET.get('edgeName')
#     edgeId = request.GET.get('edgeId')

#     if edgeName:
#         data = nsx_edge_get_by_name(edgeName)
#         response = JsonResponse(data, json_dumps_params={'indent': 3})

#     elif edgeId:
#         data = nsx_edge_get_by_id(edgeId)
#         response = JsonResponse(data)

#     return response

# @api_view(["GET"])
# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes((IsAuthenticated,))
# def logicalswitches(request):
#     data = get_logicalswitches_all()
#     return JsonResponse(data, json_dumps_params={'indent': 3})

# @api_view(["GET"])
# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes((IsAuthenticated,))
# def logicalswitch(request):
#     tzone = request.GET.get('tzone')        
#     lsName = request.GET.get('lsName')  
#     virtualwireId = request.GET.get('virtualwireId')

#     if lsName:
#         data = get_logicalswitch(lsName, tzone)
#         response = JsonResponse(data, json_dumps_params={'indent': 3})

#     elif virtualwireId:
#         data = {"virtualwireId" : virtualwireId}
#         response = JsonResponse(data, json_dumps_params={'indent': 3})

#     else:
#         response = HttpResponse("Logical switch not found.")

#     return response

# ## vCenter ##

# @api_view(["GET"])
# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes((IsAuthenticated,))
# def datacenters(request):
#     data = get_datacenters_all()
#     return JsonResponse(data)

# @api_view(["GET"])
# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes((IsAuthenticated,))
# def datacenter(request):
#     datacenterName = request.GET.get('datacenterName')
#     if datacenterName:
#         dcId = get_datacenter_id(datacenterName)        
#         data = {"datacenterName" : datacenterName, "datacenterId" : dcId}

#         return JsonResponse(data, json_dumps_params={'indent': 3})

# @api_view(["GET"])
# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes((IsAuthenticated,))
# def transportzones(request):
#     data = get_tz_all()
#     return JsonResponse(data, json_dumps_params={'indent': 3})

# ## vCPE ##

# @api_view(["GET", "POST", "PUT", "DELETE"])
# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes((IsAuthenticated,))
# # @require_http_methods(["GET", "POST", "DELETE", "PUT"])
# def clients(request):
#     if request.method == "GET":
#         data = {"clients" : []}
#         for client in Client.objects.all():
#             data["clients"].append({"client" : client.name})

#         return JsonResponse(data, json_dumps_params={'indent': 3})

#     elif request.method == "POST":
#         data = json.loads(request.body.decode(encoding='UTF-8'))
        
#         client = Client(name=data["name"])
#         client.save()

#         return HttpResponse("Client added.")

#     elif request.method == "DELETE":
#         client_name = request.GET.get("name")
#         client = Client.objects.filter(name=client_name)
#         client.delete()

#         return HttpResponse("Client deleted.")

#     elif request.method == "PUT":
#         client_name = request.GET.get("name")
#         client = Client.objects.get(name=client_name)

#         if client:
#             data = json.loads(request.body.decode(encoding='UTF-8'))

#             client.name = data["name"]
#             client.save()

#             return HttpResponse("Client updated.")
#         else:
#             return HttpResponse("Client not found.")

# @api_view(["GET", "POST", "PUT", "DELETE"])
# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes((IsAuthenticated,))
# def hubs(request):
#     if request.method == "GET":
#         data = {"hubs" : []}
#         for hub in Hub.objects.all():
#             data["hubs"].append({"hub" : hub.name,
#                                  "transport_zone" : hub.transport_zone_name,
#                                  "cluster-name" : hub.cluster_name,
#                                  "datastore-id" : hub.datastore_id,
#                                  "resourcePool-id" : hub.resource_pool_id,
#                                  "datacenter-id" : hub.datacenter_id,
#                                  "uplink-ip" : hub.uplink_ip,
#                                  "uplink-pg" : hub.uplink_pg,
#                                  "uplink-pg-id" : hub.uplink_pg_id,
#                                  "rac-ip" : hub.mx_ip,
#                                  "vxrail-ae-interface" : hub.vxrail_ae_interface})

#         return JsonResponse(data, json_dumps_params={'indent': 3})

#     elif request.method == "POST":
#         data = json.loads(request.body.decode(encoding='UTF-8'))

#         hub = Hub(name=data["hub"],
#                   transport_zone_name=data["transport_zone"],
#                   cluster_name=data["cluster-name"],
#                   datastore_id=data["datastore-id"],
#                   resource_pool_id=data["resourcePool-id"],
#                   datacenter_id=data["datacenter-id"],
#                   uplink_ip=data["uplink-ip"],
#                   uplink_pg=data["uplink-pg"],
#                   uplink_pg_id=data["uplink-pg-id"],
#                   mx_ip=data["rac-ip"],
#                   vxrail_ae_interface=data["vxrail-ae-interface"])

#         hub.save()
#         return HttpResponse("Hub added.")

#     elif request.method == "DELETE":
#         hub_name = request.GET.get("hub")
#         hub = Hub.objects.filter(name=hub_name)

#         hub.delete()

#         return HttpResponse("Hub deleted.")

#     elif request.method == "PUT":
#         hub_name = request.GET.get("hub")
#         hub = Hub.objects.filter(name=hub_name)

#         if hub:
#             data = json.loads(request.body.decode(encoding='UTF-8'))

#             hub.update(**data)

#             return HttpResponse("Hub updated.")

#         else:
#             return HttpResponse("Hub not found.")

# @api_view(["GET", "POST", "DELETE"])
# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes((IsAuthenticated,))
# def privateirsservices(request):
#     if request.method == "GET":
#         return HttpResponse("Method not yet available.")

#     elif request.method == "POST":
#         return HttpResponse("Method not yet available.")

# @api_view(["GET", "POST", "DELETE"])
# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes((IsAuthenticated,))
# def publicirsservices(request):
#     if request.method == "GET":
#         data = {"publicservices" : []}

#         for publicservice in PublicIrsService.objects.all():
#             data["publicservices"].append({"client" : publicservice.client.name,
#                                            "public_network" : publicservice.public_network.ip+"/"+str(publicservice.public_network.prefix),
#                                            "edge_name" : publicservice.edge_name,
#                                            "hub" : publicservice.portgroup.hub.name,
#                                            "sco" : publicservice.sco_port.sco.name,
#                                            "product-identifier" : publicservice.product_identifier})

#         return JsonResponse(data, json_dumps_params={'indent': 3})

#     elif request.method == "POST":

#         data = json.loads(request.body.decode(encoding='UTF-8'))

#         hub = Hub.objects.get(name=data["hub"])
#         sco = Sco.objects.get(name=data["sco"])
#         client = Client.objects.get(name=data["client"])


#         pg = Portgroup.assign_free_pg_from_hub(hub)
#         wan_ip = IpWan.assign_free_wan_ip_from_hub(hub)
#         sco_port = ScoPort.assign_free_port_from_sco(sco)
#         public_network = IpPublicSegment.assign_free_public_ip()

#         vxrail_logical_unit = LogicalUnit.assign_free_logical_unit_at_hub(hub)
#         sco_logical_unit = LogicalUnit.assign_free_logical_unit_at_hub(hub)

#         obj = PublicIrsService(edge_name="vCPE-" + data["client"] + "-" + data["product_identifier"],
#                                portgroup=pg,
#                                ip_wan=wan_ip.network,
#                                sco_port=sco_port,
#                                public_network=public_network,
#                                vxrail_logical_unit=vxrail_logical_unit.logical_unit_id,
#                                sco_logical_unit=sco_logical_unit.logical_unit_id,
#                                client=client,
#                                product_identifier=data["product_identifier"])

#         client_network = ip_network(obj.public_network.ip + "/" + str(obj.public_network.prefix))
        

#         jinja_vars = {
#                 "datacenterMoid" : hub.datacenter_id,
#                 "name" : obj.edge_name,
#                 "description" : "",
#                 "appliances" : {    "applianceSize" : 'xlarge',
#                                                         "appliance" : {"resourcePoolId" : hub.resource_pool_id,
#                                                                      "datastoreId" : hub.datastore_id
#                                                                     }},
#                 "vnics" : [{"index" : "0",
#                                 "name" : "uplink",
#                                 "type" : "Uplink",
#                                 "portgroupId" : hub.uplink_pg_id,
#                                 "primaryAddress" : obj.ip_wan,
#                                 "subnetMask" : "255.255.254.0", 
#                                 "mtu" : "1500",
#                                 "isConnected" : "true"
#                             },
#                             {"index" : "1",
#                                 "name" : "public",
#                                 "type" : "Internal",
#                                 "portgroupId" : obj.portgroup.dvportgroup_id,
#                                 "primaryAddress" : str(list(client_network.hosts())[0]),
#                                 "subnetMask" : str(client_network.netmask),
#                                 "mtu" : "1500",
#                                 "isConnected" : "true"
#                              }],

#                 "cliSettings" : {"userName" : "admin",
#                                 "password" : "T3stC@s3NSx!",
#                                 "remoteAccess" : "true"}
#         }



#         # nsx_edge_create(jinja_vars)
#         # edge_id = nsx_edge_get_id_by_name(obj.edge_name)
#         # nsx_edge_add_gateway(edge_id, "0", "100.64.4.1", "1500")

#         mx_parameters = {'mx_ip' : hub.mx_ip,
#                         'client_id' : "BD-" + data["client"] + "-" + data["product_identifier"],
#                         'service_description' : "Public IRS Service",
#                         'vxrail_logical_unit' : obj.vxrail_logical_unit,
#                         'sco_logical_unit' : obj.sco_logical_unit,
#                         'vxrail_vlan' : obj.portgroup.vlan_tag,
#                         'sco_inner_vlan' : obj.sco_port.vlan_tag,
#                         'vxrail_description' : "VxRail CEN",
#                         'sco_description' : sco.name,
#                         'vxrail_ae_interface' : hub.vxrail_ae_interface,
#                         'sco_ae_interface': sco.sco_ae_interface,
#                         'qinqOuterVlan': sco.qinqOuterVlan,
#                         "public_network_ip" : str(client_network),
#                         "ip_wan" : obj.ip_wan}

#         # configure_mx(mx_parameters, "set")

#         response = {"jinja_vars" : jinja_vars,
#                     "mx_parameters" : mx_parameters}

#         obj.save()

#         return JsonResponse(response, json_dumps_params={'indent': 3})

#     elif request.method == "DELETE":
#         client_name = request.GET.get("client")
#         client = Client.objects.get(name=client_name)
#         service = PublicIrsService.objects.get(client=client)

#         if service:
#             service.portgroup.unassign()
            
#             # set SCO port to unused
#             service.sco_port.unassign()

#             # set logical units to unused
#             LogicalUnit.unassign(service.vxrail_logical_unit, service.portgroup.hub)
#             LogicalUnit.unassign(service.sco_logical_unit, service.portgroup.hub)

#             # set Edge WAN IP to unused
#             IpWan.unassign_ip(service.ip_wan)

#             # set public segment to unused
#             service.public_network.unassign()

#             # delete edge
#             # nsx_edge_delete_by_name(service.edge_name)

#             # delete mx config

#             # load mx configuration parameters
#             mx_parameters = {'mx_ip' : service.portgroup.hub.mx_ip,
#                             'client_id' : "BD-" + service.client.name + "-" + service.product_identifier,
#                             'vxrail_logical_unit' : service.vxrail_logical_unit,
#                             'sco_logical_unit' : service.sco_logical_unit,
#                             'vxrail_ae_interface' : service.portgroup.hub.vxrail_ae_interface,
#                             'sco_ae_interface': service.sco_port.sco.sco_ae_interface,
#                             "public_network_ip" : str(ip_network(service.public_network.ip)) + "/" + \
#                                                   str(service.public_network.prefix)}

#             # configure_mx(mx_parameters, "delete")


#             service.delete()

#             return JsonResponse(mx_parameters, json_dumps_params={'indent': 3})

#         else:
#             return HttpResponse("Cannot delete service. Reason: Service not found.")
    
# @api_view(["GET", "POST", "PUT", "DELETE"])
# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes((IsAuthenticated,))
# def ippublicsegments(request):
#     if request.method == "GET":
#         data = {"ippublicsegments" : []}

#         for segment in IpPublicSegment.objects.all():
#             data["ippublicsegments"].append({"ip" : segment.ip, "prefix" : str(segment.prefix), "used" : segment.used})

#         return JsonResponse(data, json_dumps_params={'indent': 3})

#     elif request.method == "POST":
#         data = json.loads(request.body.decode(encoding='UTF-8'))

#         segment = IpPublicSegment(ip=data["ip"], prefix=data["prefix"])

#         segment.save()

#         return HttpResponse("Public segment added.")

#     elif request.method == "PUT":
#         ip = request.GET.get("segment")
#         data = json.loads(request.body.decode(encoding='UTF-8'))

#         segment = IpPublicSegment.objects.filter(ip=ip)

#         if segment:         
#             segment.update(**data)

#             return HttpResponse("Public segment updated.")

#         else:
#             return HttpResponse("Public segment not found.")

#     elif request.method == "DELETE":
#         ip = request.GET.get("segment")
#         segment = IpPublicSegment.objects.get(ip=ip)

#         if segment:
#             segment.delete()

#             return HttpResponse("Public segment deleted.")

#         else:
#             return HttpResponse("Public segment not found.")

# @api_view(["GET", "POST", "PUT", "DELETE"])
# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes((IsAuthenticated,))
# def ipwans(request):
#     if request.method == "GET":
#         data = {"ipwans" : []}

#         for ip in IpWan.objects.all():
#             data["ipwans"].append({"hub" : ip.hub.name, "ip" : ip.network, "prefix" : str(ip.prefix), "used" : ip.used})

#         return JsonResponse(data, json_dumps_params={'indent': 3})

#     elif request.method == "POST":
#         data = json.loads(request.body.decode(encoding='UTF-8'))

#         hub = Hub.objects.get(name=data["hub"])

#         if hub:
#             ipwan = IpWan(network=data["network"],
#                       prefix=data["prefix"],
#                       hub=hub)

#             ipwan.save()

#             return HttpResponse("IP WAN added.")

#         else:
#             return HttpResponse("IP WAN cannot be added. Reason: Hub not found.")

#     elif request.method == "PUT":
#         network = request.GET.get("ipWan")
#         data = json.loads(request.body.decode(encoding='UTF-8'))

#         hub = Hub.objects.get(name=data["hub"])
#         ipWan = IpWan.objects.get(network=network)

#         ipWan.hub = hub
#         ipWan.save()

#         ipWan = IpWan.objects.filter(network=network)

#         if ipWan:
#             data.pop("hub")
#             ipWan.update(**data)

#             return HttpResponse("IP WAN updated.")

#         else:
#             return HttpResponse("IP WAN not found.")

#     elif request.method == "DELETE":
#         network = request.GET.get("ipWan")
#         ipwan = IpWan.objects.get(network=network)

#         if ipwan:
#             ipwan.delete()

#             return HttpResponse("IP WAN deleted.")

#         else:
#             return HttpResponse("IP WAN not found.")

# @api_view(["GET", "POST", "PUT", "DELETE"])
# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes((IsAuthenticated,))
# def logicalunits(request):
#     if request.method == "GET":
#         data = {"logicalunits" : []}
        
#         for lu in LogicalUnit.objects.all():
#             hubs = []
#             for h in lu.hubs.all():
#                 hubs.append(h.name)

#             data["logicalunits"].append({"id" : lu.logical_unit_id, "used" : lu.used, "hubs" : hubs})

#         return JsonResponse(data, json_dumps_params={'indent': 3})

#     elif request.method == "POST":
#         data = json.loads(request.body.decode(encoding='UTF-8'))

#         lu = LogicalUnit(logical_unit_id=data["logical_unit_id"])
#         lu.save()

#         for h in data["hubs"]:
#             hub = Hub.objects.get(name=h)
#             if hub: lu.hubs.add(hub)

#         return HttpResponse("Logical unit added.")

    
#     elif request.method == "PUT":
#         lu_id = request.GET.get("logicalUnit")
#         lu = LogicalUnit.objects.get(logical_unit_id=lu_id)
        
#         data = json.loads(request.body.decode(encoding='UTF-8'))
#         if lu:
#             for hub_name in data["hubs"]:
#                     hub = Hub.objects.get(name=hub_name)
#                     lu.hubs.add(hub)

#             lu = LogicalUnit.objects.filter(logical_unit_id=lu_id)

            
#             lu.update(logical_unit_id=data["logical_unit_id"])
            
#             return HttpResponse("Logical unit updated.")

#         else:
#             return HttpResponse("Logical unit not found.")

#     elif request.method == "DELETE":
#         lu_id = request.GET.get("logicalUnit")
#         lu = LogicalUnit.objects.filter(logical_unit_id=lu_id)

#         if lu:
#             lu.delete()

#             return HttpResponse("Logical unit deleted.")

#         else:
#             return HttpResponse("Logical unit not found.")

# @api_view(["GET", "POST", "PUT", "DELETE"])
# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes((IsAuthenticated,))
# def portgroups(request):
#     if request.method == "GET":
#         data = {"portgroups" : []}

#         for pg in Portgroup.objects.all():
#             data["portgroups"].append({"id" : pg.dvportgroup_id,
#                                        "used" : pg.used,
#                                        "name" : pg.name,
#                                        "vlan-id" : pg.vlan_tag,
#                                        "hub" : pg.hub.name})

#         return JsonResponse(data, json_dumps_params={'indent': 3})

#     elif request.method == "POST":
#         data = json.loads(request.body.decode(encoding='UTF-8'))

#         hub = Hub.objects.get(name=data["hub"])

#         if hub:
#             pg = Portgroup(vlan_tag=data["vlan_tag"],
#                       name=data["name"],
#                       hub=hub,
#                       dvportgroup_id=data["dvportgroup_id"])

#             pg.save()

#             return HttpResponse("Portgroup added.")

#         else:

#             return HttpResponse("Portgroup cannot be added. Reason: Hub not found.")

#     elif request.method == "PUT":
#         pg_name = request.GET.get("portgroupName")
#         pg = Portgroup.objects.filter(name=pg_name)

#         if pg:
#             data = json.loads(request.body.decode(encoding='UTF-8'))

#             pg.update(**data)

#             return HttpResponse("Portgroup updated.")

#         else:
#             return HttpResponse("Portgroup not found.")

#     elif request.method == "DELETE":
#         pg_name = request.GET.get("portgroupName")
#         pg = Portgroup.objects.filter(name=pg_name)

#         if pg:
#             pg.delete()

#             return HttpResponse("Portgroup deleted.")

#         else:
#             return HttpResponse("Portgroup not found.")

# @api_view(["GET", "POST", "PUT", "DELETE"])
# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes((IsAuthenticated,))
# def scoports(request):
#     if request.method == "GET":
#         data = {"sco_ports" : []}

#         for sco_port in ScoPort.objects.all():
#             data["sco_ports"].append({"sco" : sco_port.sco.name,
#                                       "port" : sco_port.port,
#                                       "vlan_id" : sco_port.vlan_tag,
#                                       "description" : sco_port.description,
#                                       "used" : sco_port.used})

#         return JsonResponse(data, json_dumps_params={'indent': 3})

#     elif request.method == "POST":
#         data = json.loads(request.body.decode(encoding='UTF-8'))

#         sco = Sco.objects.get(name=data["sco"])

#         if sco:
#             sco_port = ScoPort(port=data["port"],
#                       description=data["description"],
#                       vlan_tag=data["vlan_tag"],
#                       sco=sco)

#             sco_port.save()

#             return HttpResponse("SCO Port added.")

#         else:

#             return HttpResponse("SCO Port cannot be added. Reason: SCO not found.")

#     elif request.method == "PUT":
#         port = request.GET.get("port")
#         sco_port = ScoPort.objects.filter(port=port)

#         if sco_port:
#             data = json.loads(request.body.decode(encoding='UTF-8'))

#             sco_port.update(**data)

#             return HttpResponse("SCO Port updated.")

#         else:
#             return HttpResponse("SCO Port not found.")

#     elif request.method == "DELETE":
#         port = request.GET.get("port")
#         sco_port = ScoPort.objects.filter(port=port)

#         if sco_port:
#             sco_port.delete()

#             return HttpResponse("SCO Port deleted.")

#         else:
#             return HttpResponse("SCO Port not found.")

# @api_view(["GET", "POST", "PUT", "DELETE"])
# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes((IsAuthenticated,))
# def scos(request):
#     if request.method == "GET":
#         data = {"scos" : []}

#         for sco in Sco.objects.all():
#             data["scos"].append({"id" : sco.accessNodeId,
#                                  "name" : sco.name,
#                                  "sco_ae_interface" : sco.sco_ae_interface,
#                                  "qinqOuterVlan" : sco.qinqOuterVlan,
#                                  "hub" : sco.hub.name})

#         return JsonResponse(data, json_dumps_params={'indent': 3})

#     elif request.method == "POST":
#         data = json.loads(request.body.decode(encoding='UTF-8'))

#         hub = Hub.objects.get(name=data["hub"])

#         if hub:
#             sco = Sco(name=data["name"],
#                       accessNodeId=data["accessNodeId"],
#                       sco_ae_interface=data["sco_ae_interface"],
#                       qinqOuterVlan=data["qinqOuterVlan"],
#                       hub=hub)

#             sco.save()

#             return HttpResponse("SCO added.")

#         else:

#             return HttpResponse("SCO cannot be added. Reason: Hub not found.")

#     elif request.method == "PUT":
#         sco_name = request.GET.get("sco")
#         sco = Sco.objects.filter(name=sco_name)

#         if sco:
#             data = json.loads(request.body.decode(encoding='UTF-8'))

#             sco.update(**data)

#             return HttpResponse("SCO updated.")

#         else:
#             return HttpResponse("SCO not found.")

#     elif request.method == "DELETE":
#         sco_name = request.GET.get("sco")
#         sco = Sco.objects.filter(name=sco_name)

#         if sco:
#             sco.delete()

#             return HttpResponse("SCO deleted.")

#         else:
#             return HttpResponse("SCO not found.")

# ######
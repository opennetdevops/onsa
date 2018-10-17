# from django.conf import settings
# from django.core import serializers
# from django.http import HttpResponse, JsonResponse
# from django.views import View
# from ..models import Service
# from enum import Enum
# import json
# import requests

# from pprint import pprint

# VRF_SERVICES = ['cpeless_mpls', 'cpe_mpls', 'vpls']
# AS_SERVICES = ['cpe_mpls']
# CLIENT_NETWORK_SERVICES = ['cpeless_mpls']
# PREFIX_SERVICES = ['cpeless_irs', 'vcpe_irs', 'cpeless_mpls']

# class ServiceProcessView(View):
    
#     def post(self, request,service_id):
#         data = json.loads(request.body.decode(encoding='UTF-8'))
#         client_node_sn = data['cpe_sn']

#         service = Service.objects.get(id=service_id)
        
#         #Get CPE from inventory
#         cpe_data = _get_cpe(client_node_sn)

#         #update inventory with Cpe Client
#         if cpe_data is not None:
#             cpe_data['client'] = service.client.name
#             _update_cpe(client_node_sn, cpe_data)
#         else:
#             response = {"message" : "Service - CPE relation PUT failed"}
#             return JsonResponse(response)

#         #Create ports - and assign one
#         print("get cpe Port from cpe: ", cpe_data)
#         cpe_port = _get_free_cpe_port(client_node_sn)
#         cpe_port_id = cpe_port['id']
#         client_node_port = cpe_port['interface_name']
#         print("mark port as used: ",cpe_port)

#         #Assign CPE Port (mark as used)
#         _use_port(client_node_sn, cpe_port_id)

#         # update Product
#         _update_product_cpe_data(service_id, client_node_sn, client_node_port)


#         # service.client_node_sn = client_node_sn
#         # service.client_node_port = cpe_port['interface_name']
#         print("BEGIN - request charle service")
#         r = _request_charles_service(service)
#         print("END - request charle service")

#         if r.ok:
#             service.service_state = "REQUESTED" #TODO use enum or similar but not hardcode
#         else:
#             service.service_state = "ERROR" #TODO use enum or similar but not hardcode

#         service.save()
#         response = {"message" : "Service - CPE relation requested"}
        
#         return JsonResponse(response)

# def _get_free_cpe_port(client_node_sn):
#     url= settings.INVENTORY_URL + "clientnodes/" + client_node_sn + "/clientports?used=False"
#     rheaders = {'Content-Type': 'application/json'}
#     response = requests.get(url, auth = None, verify = False, headers = rheaders)
#     json_response = json.loads(response.text)
#     if json_response:
#         return json_response[0]
#     else:
#         return None

# def _get_cpe(client_node_sn):
#     url= settings.INVENTORY_URL + "clientnodes/" + client_node_sn
#     rheaders = {'Content-Type': 'application/json'}
#     response = requests.get(url, auth = None, verify = False, headers = rheaders)
#     json_response = json.loads(response.text)
#     if json_response:
#         return json_response
#     else:
#         return None

# def _update_cpe(client_node_sn, data):
#     url= settings.INVENTORY_URL + "clientnodes/" + client_node_sn
#     rheaders = {'Content-Type': 'application/json'}
#     response = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
#     json_response = json.loads(response.text)
#     if json_response:
#         return json_response
#     else:
#         return None


# def _update_product_cpe_data(product_id, client_node_sn, client_node_port):
#     url= settings.INVENTORY_URL + "products/" + product_id
#     rheaders = {'Content-Type': 'application/json'}
#     data = { "client_node_sn":client_node_sn,
#              "client_node_port":client_node_port
#             }
#     response = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
#     json_response = json.loads(response.text)
#     if json_response:
#         return json_response
#     else:
#         return None



# def _get_service(service_id):
#     url = settings.CORE_URL + service_id
#     rheaders = {'Content-Type': 'application/json'}
#     response = requests.get(url, auth = None, verify = False, headers = rheaders)
#     json_response = json.loads(response.text)
#     if json_response:
#         return json_response[0]
#     else:
#         return None

# def _generate_json_data(service):

#     product = _get_product(service.id)
#     bandwidth = product['bandwidth']
#     access_node_id = product['access_node_id']
#     access_port_id = product['access_port_id']
#     client_node_sn = product['client_node_sn']
#     client_node_port = product['client_node_port']
#     access_node = _get_access_node(access_node_id)
#     print("access node",access_node)
#     location = _get_location(access_node['location_id'])

#     data = { 'data_model' : {
#                         "service_id" : service.id,
#                         "service_type" : service.service_type,
#                         "client_id" : service.client.id,
#                         "client_name" : service.client.name,
#                         "location": location['name']
#                     },

#             "access_port_id": access_port_id,
#             "access_node_id": access_node_id,
#             "client_node_port" : client_node_port,
#             "client_node_sn" : client_node_sn,
#             "bandwidth" : bandwidth
#     }
    
#     if service.service_type in CLIENT_NETWORK_SERVICES:        
#         data["client_network"] = service.client_network

#     if service.service_type in PREFIX_SERVICES:
#         data["prefix"] = service.prefix

#     if service.service_type in VRF_SERVICES:
#         vrf = _get_vrf(product['vrf_id'])
#         vrf_name = vrf['name']
#         data['vrf_name'] = vrf_name
#         service.vrf_name = vrf_name
#         if service.service_type in AS_SERVICES:
#             service.autonomous_system = _assign_autonomous_system(vrf_name) 
#             data['client_as']  =  service.autonomous_system 

#     return data


# def _request_charles_service(service):
#     rheaders = {'Content-Type': 'application/json'}
#     print("service:", service)

#     data = _generate_json_data(service)
#     pprint(data)
#     url = settings.CHARLES_URL + "services"
#     r = requests.post(url, data = json.dumps(data), headers=rheaders)
#     print("r:", r)
#     return r

# def _use_port(client_node_id, client_port_id):
#     url= settings.INVENTORY_URL + "clientnodes/" + str(client_node_id) + "/clientports/" + str(client_port_id)
#     rheaders = {'Content-Type': 'application/json'}
#     data = {"used":True}
#     response = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
#     print(response.text)
#     json_response = json.loads(response.text)
#     if json_response:
#         return json_response
#     else:
#         return None

# def _assign_autonomous_system(vrf_name):    
#     list_as = list( Service.objects.filter(vrf_name=vrf_name).values('autonomous_system') )
#     print("list_as",list_as)
    
#     if (len(list_as) == 1) and (list_as[0]['autonomous_system'] is 0):
#         return 65000

#     ordered_list_as = sorted(list_as, key=lambda k: k['autonomous_system'])
#     last_as = int( ordered_list_as[-1]['autonomous_system'] )

#     if last_as <= 65500:
#         return (last_as + 1)
#     else:
#         while(1):
#             proposed_as = 65000
#             if proposed_as > 65500:
#                 #TODO throw exception
#                 return -1

#             if Service.objects.filter(vrf_name=vrf_name, autonomous_system=proposed_as).values().count():
#                 proposed_as+=1
#             else:
#                 return proposed_as


# def _get_product(service_id):
#     url = settings.INVENTORY_URL + "products/" + service_id
#     rheaders = {'Content-Type': 'application/json'}
#     response = requests.get(url, auth = None, verify = False, headers = rheaders)
#     json_response = json.loads(response.text)
#     if json_response:
#         return json_response
#     else:
#         return None


# def _get_access_node(access_node_id):
#     url = settings.INVENTORY_URL + "accessnodes/" + str(access_node_id)
#     rheaders = {'Content-Type': 'application/json'}
#     response = requests.get(url, auth = None, verify = False, headers = rheaders)
#     json_response = json.loads(response.text)
#     if json_response:
#         return json_response
#     else:
#         return None


# def _get_vrf(vrf_id):
#     url = settings.INVENTORY_URL + "vrfs/" + str(vrf_id)
#     rheaders = {'Content-Type': 'application/json'}
#     response = requests.get(url, auth = None, verify = False, headers = rheaders)
#     json_response = json.loads(response.text)
#     if json_response:
#         return json_response
#     else:
#         return None


# def _get_location(location_id):
#     url = settings.INVENTORY_URL + "locations/" + str(location_id)
#     rheaders = {'Content-Type': 'application/json'}
#     response = requests.get(url, auth = None, verify = False, headers = rheaders)
#     json_response = json.loads(response.text)
#     if json_response:
#         return json_response
#     else:
#         return None
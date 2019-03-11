from django.conf import settings
from django.http import JsonResponse

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from core.utils import *
from core.views.ldap_jwt import *

import json
import requests


class ServiceResourcesView(APIView):
    authentication_classes = ([JSONWebTokenLDAPAuthentication, ])
    permission_classes = (IsAuthenticated,)

    def get(self, request, service_id=None):
        if service_id is not None:
            service = get_service(service_id)
            json_response = self.get_resources(service)
        return JsonResponse(json_response, safe=False)

    def get_resources(self, service):

        service = pop_empty_keys(service)

        router_node = get_router_node(service['router_node_id'])
        access_node = get_access_node(service['access_node_id'])
        access_port = get_access_port(service['access_port_id'])
        location = get_location(service['location_id'])
        customer_location = get_customer_location(
            service['client_id'], service['customer_location_id'])
        client = get_client(service['client_id'])

        resources = {
            "customer": client['name'],
            "location": location['name'],
            "customer_location": customer_location['address'],
            "router_node": {'name': router_node['name']},
            "access_node": {"model": access_node['model'],
                            "name": access_node['name'],
                            "access_port": access_port['port']},
            "vlan_id": service['vlan_id'],
        }

        if service['service_type'] in VRF_SERVICES:
            resources['client_network'] = service['client_network']
        elif service['service_type'] in IRS_SERVICES:
            if 'public_network' in service.keys():
                resources['public_network'] = service['public_network']

        if service['service_state'] in BB_STATES:
            resources['router_node']['logical_unit_id'] = service['logical_unit_id']
            if service['service_type'] == "vcpe_irs":
                resources['router_node']['vcpe_logical_unit_id'] = service['vcpe_logical_unit_id']
        elif service['service_state'] in CPE_STATES:
            client_node = get_client_node(service['client_node_sn'])

            resources["client_node"] = {"model": client_node['model'],
                                        "wan_port": client_node['uplink_port'],
                                        "SN": client_node['serial_number']}

            if 'client_port_id' in service.keys():
                client_port = get_client_port(
                    service['client_node_sn'], service['client_port_id'])
                resources['client_node']['client_port'] = client_port['interface_name']

        return resources


service_resources_view = ServiceResourcesView.as_view()

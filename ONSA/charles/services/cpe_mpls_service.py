from charles.utils.utils import *
from charles.views.service import *

def generate_cpe_mpls_request(client, service):
    location = get_location(service['location_id'])
    router_node = get_router_node(service['router_node_id'])
    access_port = get_access_port(service['access_port_id'])
    access_node = get_access_node(service['access_node_id'])
    client_node = get_client_node(service['client_node_sn'])
    client_port = get_client_port(service['client_node_sn'], service['client_port_id'])        
    
    vrf = get_vrf(service['vrf_id'])

    """
    Fetch for logical units
    """
    free_logical_units = get_free_logical_units(router_node['id'])
    logical_unit_id = free_logical_units[0]['logical_unit_id']

    vrf_exists = vrf_exists_in_location(vrf['rt'], location['id'])

    error = False

    if logical_unit_id:
        wan_network = get_wan_mpls_network(location['name'], client['name'], service['id'])
        if wan_network: 
            if not vrf_exists:
                add_location_to_vrf(vrf['rt'], location['id'])
            #Add logical unit to router node
            add_logical_unit_to_router_node(router_node['id'], logical_unit_id, service['id'])
            
            client_as_number = service['autonomous_system']

            service_data = { 'logical_unit_id': logical_unit_id,
                             'client_network': service['client_network'], 
                             'wan_network': wan_network,
                             'autonomous_system': client_as_number}

            
            update_service(service['id'], service_data)
#/////
            config = {
               "client" : client['name'],
               "service_type" :  service['service_type'],
               "service_id" : service['id'],
               "op_type" : "CREATE",
               "parameters" : {
                        "pop_size" : location['pop_size'],       
                                "an_uplink_interface" : access_node['uplink_interface'],
                                "an_uplink_ports" :   access_node['uplink_ports'],
                                "logical_unit" : logical_unit_id,   
                                "provider_vlan" : access_node['provider_vlan'],      
                                "service_vlan" : service['vlan_id'], 
                                "bandwidth" : service['bandwidth'],
                                "client_as_number" : client_as_number,
                                "an_client_port" : access_port['port'],
                                "on_client_port" : client_port['interface_name'],
                                "vrf_exists": vrf_exists,
                                "wan_cidr": wan_network,
                                "client_cidr": service['client_network'],
                    "vrf_name": vrf['name'],
                    "vrf_id": vrf['rt'],
                    "loopback":router_node['loopback']
                            },
                "devices" : [{"vendor":router_node['vendor'],"model":router_node['model'],"mgmt_ip":router_node['mgmt_ip']},
                             {"vendor":access_node['vendor'],"model":access_node['model'],"mgmt_ip":access_node['mgmt_ip']},
                             {"vendor":client_node['vendor'],"model":client_node['model'],"mgmt_ip":client_node['mgmt_ip']}]}

            pprint(config)
            #Call worker
            configure_service(config)
        else:
            error = True
    else:
        error = True

    if error:
        service.service_state = ServiceStatuses['ERROR'].value
        service.save()
        print("Not possible service")

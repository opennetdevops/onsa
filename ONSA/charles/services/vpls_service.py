from utils import *
from charles.views.service import *

def generate_vpls_request(client, service):
    location = get_location(service['location'])
    router_node = get_router_node(services['router_node_id'])
    access_port = get_access_port(service['access_port_id'])
    access_node = get_access_node(service['access_node_id'])
    client_node = get_client_node(service['client_node_sn'])
    client_port = get_client_port(service['client_port_id'])        
    
    client_as = service['autonomous_system']
    vrf = get_vrf(service['vrf_id'])

    """
    Fetch for logical units
    """
    free_logical_units = get_free_logical_units(router_node['id'])
    logical_unit_id = free_logical_units[0]['logical_unit_id']

    
    vrf_exists = vrf_exists_in_location(vrf['rt'],location['id'])

    if  logical_unit_id:
        service_data = { 'logical_unit_id': logical_unit_id }

        update_service(service['id'], service_data)

        #Add logical unit to router node
        add_logical_unit_to_router_node(router_node_id, free_logical_units[0]['logical_unit_id'], service['id'])
        if not vrf_exists:
            add_location_to_vrf(vrf['rt'], location['id'])

        config = {
           "client" : client['name'],
           "service_type" : service['service_type'],
           "service_id" : service['service_id'],
           "op_type" : "CREATE",
           "parameters" : {
                    "pop_size" : service['pop_size'],       
                            "an_uplink_interface" : access_node['uplink_interface'],
                            "an_uplink_ports" :   access_node['uplink_ports'],
                            "logical_unit" : logical_unit_id,   
                            "provider_vlan" : access_node['provider_vlan'],      
                            "service_vlan" : service['vlan_id'], 
                            "bandwidth" : service['bandwidth'],
                            "an_client_port" : access_port['port'],
                            "on_client_port" : client_port['interface_name'],
                            "vrf_exists": vrf_exists,
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
        service.service_state = ServiceStatuses['ERROR'].value
        service.save()
        print("Not possible service")

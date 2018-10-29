from charles.utils.utils import *
from charles.views.service import *

def generate_vcpe_irs_request(client, service):
    location = get_location(service['location_id'])
    router_node = get_router_node(service['router_node_id'])
    access_port = get_access_port(service['access_port_id'])
    access_node = get_access_node(service['access_node_id'])
    client_node = get_client_node(service['client_node_sn'])
    client_port = get_client_port(service['client_port_id'])        

    """
    Fetch for logical units
    """
    free_logical_units = get_free_logical_units(router_node['id'])
    logical_unit_id = free_logical_units[0]['logical_unit_id']
    vcpe_logical_unit_id = free_logical_units[1]['logical_unit_id']
    
    virtual_pod = get_virtual_pod(location['id'])
    downlink_pg = get_virtual_pod_downlink_portgroup(virtual_pod['id'])
    
    error = False

    if len(free_logical_units) >= 2 and downlink_pg:
        wan_ip = get_ip_wan_nsx(location['name'], client['name'], service['id'])
        if wan_ip:
            client_network = get_client_network(client['name'], service['id'], service['prefix'])
            if client_network:
                
                service_data = { 'logical_unit_id': logical_unit_id,
                                 'vcpe_logical_unit_id': vcpe_logical_unit_id,
                                 'public_network': client_network, 
                                 'wan_ip': wan_ip,
                                 'portgroup_id': downlink_pg['id'] }

                update_service(service['id'], service_data)

                use_portgroup(downlink_pg['id'])

                add_logical_unit_to_router_node(router_node['id'], logical_unit_id, service['id'])
                add_logical_unit_to_router_node(router_node['id'], vcpe_logical_unit_id, service['id'])
                config = { 
                          "client" : client['name'],
                          "service_type" : service['service_type'],
                          "service_id" : service['id'],
                          "op_type" : "CREATE",
                          "parameters":{
                                    "vmw_uplink_interface" : virtual_pod['uplink_interface'],
                                    "vmw_logical_unit" : vcpe_logical_unit_id,  
                                    "vmw_vlan" : downlink_pg['vlan_tag'],           
                                    "an_uplink_interface" : access_node['uplink_interface'],  
                                    "an_uplink_ports" :   access_node['uplink_ports'],
                                    "an_logical_unit" : free_logical_units[1]['logical_unit_id'],   
                                    "provider_vlan" : access_node['provider_vlan'],      
                                    "service_vlan" : free_vlan_tag['vlan_tag'], 
                                    "client_cidr" : client_network,
                                    "wan_ip" : wan_ip,
                                    "bandwidth" : service['bandwidth'],
                                    "datacenter_id" : virtual_pod['datacenterId'] ,
                                    "resgroup_id" : virtual_pod['resourcePoolId'],
                                    "datastore_id" : virtual_pod['datastoreId'],
                                    "wan_portgroup_id" : virtual_pod['uplink_pg_id'],
                                    "lan_portgroup_id" : downlink_pg['dvportgroup_id'],
                                    "an_client_port" : free_access_port['port'],
                                    "on_client_port" : client_port['interface_name'],
                                    "on_uplink_port" : client_node['uplink_port']
                                 },
                          "devices" : [{"vendor":router_node['vendor'],"model":router_node['model'],"mgmt_ip":router_node['mgmt_ip']},
                                       {"vendor":access_node['vendor'],"model":access_node['model'],"mgmt_ip":access_node['mgmt_ip']},
                                       {"vendor":client_node['vendor'],"model":client_node['model'],"mgmt_ip":client_node['mgmt_ip']},
                                       {"vendor":virtual_pod['vendor'],"model":virtual_pod['model'],"mgmt_ip":virtual_pod['mgmt_ip']}]
                }
                pprint(config)
                #Call worker
                configure_service(config)
            else:
                #Free wan_ip
                release_ip(client_name,service['id'])
                error = True
        else:
            error = True
    else:
        error = True

    if error:
        service.service_state = ServiceStatuses['ERROR'].value
        service.save()
        print("Not possible service")
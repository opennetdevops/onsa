# Python imports
import logging

# ONSA imports
from charles.utils.utils import *
from charles.utils.inventory_utils import *
from charles.utils.ipam_utils import *
from charles.constants import *
from charles.models import *



def deleted_automated_request(service):
  logging.debug("deleted_automated_request")
  client = get_client(service['client_id'])
  service_data = {}

  try:
    parameters = an_parameters(client, service)
    config = {
      "client": client['name'],
      "service_type":  service['service_type'],
      "service_id": service['service_id'],
      "op_type": "DELETE"}

    config['parameters'] = {
                "service_vlan": service['vlan_id'],
                "an_client_port": parameters['an_client_port'],
                "an_uplink_ports": parameters['an_uplink_ports'],
                "access_port_services":parameters['access_port_services']
                  }
    config['devices'] = [{"vendor": parameters['vendor'],
        "model": parameters['model'], "mgmt_ip": parameters['mgmt_ip']}]

    service_state = DELETEINPROGRESS_SERVICE_STATE

    logging.debug("releasing service resources")
    release_access_port(service['access_port_id'])
    release_vlan(service['access_node_id'], service['vlan_id'])
    logging.debug("deleting service")
        
    #Send message(job) to Queue so workers can take it
    configure_service(config) 
  except BaseException:
    service_state = DELETEERROR_SERVICE_STATE

  service_data['service_state'] = service_state
  update_jeangrey_service(service['service_id'], service_data)
  service = update_charles_service(service, service_state)
  return service



def an_activated_automated_request(service):
  logging.debug("an_activated_automated_request")
  client = get_client(service['client_id'])
  service_data = {}

  try:
    parameters = an_parameters(client, service)
    config = {
      "client": client['name'],
      "service_type":  service['service_type'],
      "service_id": service['service_id'],
      "op_type": "CREATE"}

    config['parameters'] = {
                "service_vlan": service['vlan_id'],
                "an_client_port": parameters['an_client_port'],
                "an_uplink_ports": parameters['an_uplink_ports'],
                "access_port_services":parameters['access_port_services']
                  }
    config['devices'] = [{"vendor": parameters['vendor'],
        "model": parameters['model'], "mgmt_ip": parameters['mgmt_ip']}]

    service_state = "an_activation_in_progress"
    logging.debug("configuring service")
    
    #Send message(job) to Queue so workers can take it
    configure_service(config) 
  except BaseException:
    service_state = "ERROR"

  service_data['service_state'] = service_state
  update_jeangrey_service(service['service_id'], service_data)
  service = update_charles_service(service, service_state)
  return service

def an_parameters(client, service):
  try:
    access_port = get_access_port(service['access_port_id'])
    access_node = get_access_node(service['access_node_id'])
    an_device_model = get_device_model(access_node['device_model_id'])
    access_port_services = get_access_port_services(service['access_port_id'])

    services = ""
    for my_service in access_port_services:
      if my_service['id'] is not service['service_id']:
        services+= str(my_service['id']) + "-"
    services += str(service['service_id'])

    parameters = { 'provider_vlan': access_node['provider_vlan'],
                  'an_client_port': access_port['port'],
                  'an_uplink_ports': access_node['uplink_ports'],
                  'mgmt_ip': access_node['mgmt_ip'],
                  'model': an_device_model['model'],
                  'vendor': an_device_model['brand'],
                  'access_port_services': services }

    logging.debug(f'parameters: {parameters}')

    return parameters
  except BaseException:
    logging.error("Unable to fetch parameters")
    raise InvalidParametersException("Unable to fetch parameters")



def bb_data_ack_automated_request(service):
  pass


def bb_activated_automated_request(service):
  pass

def an_data_ack_automated_request(service):
  pass


def cpe_data_ack_automated_request(service):
  pass

def service_activated_automated_request(service):
  pass

def bb_parameters(client, service):
  pass



def cpe_parameters(client, service):
  pass 
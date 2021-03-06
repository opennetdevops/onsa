# from django.test import SimpleTestCase, LiveServerTestCase
import unittest

from charles.models import Service
from charles.utils import *
import logging

# from time import sleep


def create_mock_service(service_type, service_id, data):
    data['service_type'] = service_type
    data['id'] = service_id
    token = login_core()
    create_core_service(data, token)


class TestFailCpeIrsAutomatedServiceMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # create client
        cls.client_name = "test_client"
        create_client(cls.client_name)
        cls.client_id = get_client_by_name(cls.client_name)['id']
        cls.client_node_sn = "CCCC333CCCC"
        cls.initial_id = 1

        # create location
        data = {"name": "LAB", "address": "Gral. Hornos 690", "pop_size": "large"}
        cls.location = create_location(data)

        # create access node
        data = {"name": "LAB-SCO", "device_type": "AccessNode", "mgmt_ip": "10.120.80.56", "model": "s4224",
                "location_id": cls.location["id"], "provider_vlan": "1", "logical_unit_id": "10",
                "uplink_interface": "ae1", "vendor": "transition",
                "uplink_ports": "10GigabitEthernet 1/3, 10GigabitEthernet 1/4"}
        cls.access_node = create_access_node(data)

        # create router node
        data = {"name": "LAB-HOR", "device_type": "RouterNode", "mgmt_ip": "10.120.80.61", "model": "mx104",
                "location_id": cls.location["id"], "private_wan_ip": "100.64.0.1", "vendor": "juniper",
                "loopback": "10.120.104.1"}
        cls.router_node = create_router_node(data)
        # print(cls.router_node)

        # create client node
        data = {"name": "LAB-HOR-NID", "device_type": "ClientNode", "mgmt_ip": "10.120.80.121",
                "location_id": cls.location["id"], "model": "s3290-5", "serial_number": cls.client_node_sn,
                "vendor": "transition", "uplink_port": "2.5GigabitEthernet 1/1"}
        cls.client_node = create_client_node(data)
        # print(cls.client_node)

        # create customer location
        cls.customer_location_id = create_customer_location(cls.client_id)[
            'id']

    def setUp(self):
        # create VLAN
        data = {"vlan_tag": "3100"}
        self.vlan_tag = create_vlan_tag(data)
        # print(self.vlan_tag)

        # add VLAN to access_node --> this means: "use vlan"
        # data = {"vlan_id":self.vlan_tag["id"]}
        # add_vlan_to_access_node(self.access_node_id,data)

        # create LogicalUnit
        data = {"logical_unit_id": 15000}
        self.lu = create_logicalunit(data)

        # add LU to routerNode --> this means: "use LU"
        # add_logical_unit_to_router_node(self.router_node_id,self.lu["id"])

        # create access_port
        data = {"used": "false", "port": "GigabitEthernet 1/19"}
        self.access_port = create_access_port_at_access_node(
            self.access_node["id"], data)

        # create client node port
        data = {"interface_name": "GigabitEthernet 1/1",
                "used": "false", "service_id": ""}
        self.client_node_port = create_client_port_at_client_node(
            self.client_node["serial_number"], data)

        # define service data
        self.service_data = {
            "client": self.client_name,
            "bandwidth": 10,
            "location": self.location["name"],
            "customer_location_id": self.customer_location_id,
            "prefix": 29
        }

        self.service_id = "SVC01-A_" + str(self.initial_id)
        self.service_data['client_node_sn'] = self.client_node["serial_number"]

    def tearDown(self):
        service = get_service(self.service_id)

        # free access port
        release_access_port(service['access_port_id'])

        # delete VLAN
        delete_vlan_tag(self.vlan_tag["id"])

        # delete LogicalUnit
        delete_logicalunit(self.lu["id"])

        # delete access_port
        delete_access_port(self.access_port["id"])

        # delete client_port
        delete_client_port(self.client_node_sn, self.client_node_port["id"])

        # delete service at charles & JeanGrey
        delete_charles_service(self.service_id)
        delete_jeangrey_service(self.service_id)
        self.__class__.initial_id = self.__class__.initial_id + 1

    @classmethod
    def tearDownClass(cls):
        # delete access node
        delete_access_node(cls.access_node["id"])

        # delete router node
        delete_router_node(cls.router_node["id"])

        # create client node
        delete_client_node(cls.client_node["serial_number"])

        # delete location
        delete_location(cls.location["id"])

        # delete customer location
        delete_customer_location(cls.client_id, cls.customer_location_id)

        # delete client
        delete_client(cls.client_id)
        # pass

    def test_001_initial_service_state(self):

        # add VLAN to access_node --> this means: "use vlan"
        data = {"vlan_id": self.vlan_tag["id"]}
        add_vlan_to_access_node(self.access_node["id"], data)

        # create mock service
        create_mock_service("cpe_irs", self.service_id, self.service_data)

        service_manual = get_service(self.service_id)
        self.assertEqual(service_manual['service_state'], "ERROR")

    def test_002_fail_not_enough_vlans(self):

        logging.info(get_free_vlan(self.access_node["id"]))

        push_service_to_orchestrator(
            self.service_id, "automated", "service_activated")

        service = get_service(self.service_id)
        self.assertEqual(service['service_state'], "an_activation_in_progress")

        # release client node port for further tests
        release_client_node_port(
            self.client_node_sn, service['client_port_id'])

#     def test_003_automated_from_in_construction_to_service_activated_error(self):
#         push_service_to_orchestrator(
#             self.service_id, "automated", "service_activated")
#         service = get_service(self.service_id)
#         self.assertEqual(service['service_state'], "an_activation_in_progress")
#         update_charles_service_state(self.service_id, "ERROR")
#         service = get_service(self.service_id)
#         self.assertEqual(service['service_state'], "ERROR")

#     def test_004_hybrid_manual_till_an_data_ack_then_automated(self):
#         push_service_to_orchestrator(self.service_id, "manual", "an_data_ack")
#         service = get_service(self.service_id)
#         self.assertEqual(service['service_state'], "an_data_ack")

#         push_service_to_orchestrator(
#             self.service_id, "automated", "service_activated")

#         service = get_service(self.service_id)
#         self.assertEqual(service['service_state'], "an_activation_in_progress")
#         update_charles_service_state(self.service_id, "COMPLETED")

#         service = get_service(self.service_id)
#         self.assertEqual(service['service_state'], "bb_activation_in_progress")
#         update_charles_service_state(self.service_id, "COMPLETED")

#         service = get_service(self.service_id)
#         self.assertEqual(service['service_state'],
#                          "cpe_activation_in_progress")
#         update_charles_service_state(self.service_id, "COMPLETED")

#         service = get_service(self.service_id)
#         self.assertEqual(service['service_state'], "service_activated")

#         # release client node port for further tests
#         release_client_node_port(
#             self.client_node_sn, service['client_port_id'])

#     def test_005_manual_till_an_activated(self):
#         push_service_to_orchestrator(self.service_id, "manual", "an_data_ack")
#         service = get_service(self.service_id)
#         self.assertEqual(service['service_state'], "an_data_ack")
#         push_service_to_orchestrator(self.service_id, "manual", "an_activated")
#         service = get_service(self.service_id)
#         self.assertEqual(service['service_state'], "an_activated")

#     # def test_006_automated_till_an_activated(self):
#     #     push_service_to_orchestrator(self.service_id, "automated", "an_activated")
#     #     service = get_service(self.service_id)
#     #     self.assertEqual(service['service_state'], "an_activation_in_progress")
#     #     update_charles_service_state(self.service_id, "COMPLETED")
#     #     service = get_service(self.service_id)
#     #     self.assertEqual(service['service_state'], "an_activated")

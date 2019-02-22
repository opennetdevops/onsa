# from django.test import SimpleTestCase, LiveServerTestCase
import unittest

from charles.models import Service
from charles.utils import *
# from time import sleep


def create_mock_service(service_type, service_id, data):
    data['service_type'] = service_type
    data['id'] = service_id
    token = login_core()
    create_core_service(data, token)


@unittest.skip("testing irs")
class TestCpeMplsAutomatedServiceMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        #create client
        create_client("test_client_03")
        cls.client_id = get_client_by_name("test_client_03")['id']
        cls.client_node_sn = "CCCC3333CCCC"
        cls.location = "LAB"


    def setUp(self):
        #create customer location
        self.customer_location_id = create_customer_location(self.client_id)['id']

        #define service data
        self.service_data =  {
                            "client": "test_client_03",
                            "bandwidth": 10,
                            "location": self.location,
                            "customer_location_id": self.customer_location_id
                            }

        self.service_id = "SVC01-A"
        self.service_data['client_node_sn'] = self.client_node_sn
        create_mock_service("cpe_mpls", self.service_id, self.service_data )

    def tearDown(self):
        service = get_service(self.service_id)

        #free access port
        release_access_port(service['access_port_id'])

        #delete customer location
        delete_customer_location(self.client_id, self.customer_location_id)
        # print("jean grey services: ", get_services())
        # print("charles services: ", get_charles_services())

        #delete service at charles & JeanGrey
        delete_charles_service(self.service_id)

        # sleep(10)




    @classmethod
    def tearDownClass(cls):
        #delete client
        delete_client(cls.client_id)

    def test_001_initial_service_state(self):      
        service_manual = get_service(self.service_id)
        self.assertEqual(service_manual['service_state'], "in_construction")

    def test_002_automated_from_in_construction_to_service_activated_ok(self):
        push_service_to_orchestrator(self.service_id, "automated", "service_activated")
        service = get_service(self.service_id)
        self.assertEqual(service['service_state'], "bb_activation_in_progress")
        update_charles_service_state(self.service_id, "COMPLETED")
        service = get_service(self.service_id)
        self.assertEqual(service['service_state'], "cpe_activation_in_progress")
        update_charles_service_state(self.service_id, "COMPLETED")
        service = get_service(self.service_id)
        self.assertEqual(service['service_state'], "service_activated")
        #release client node port for further tests
        release_client_node_port(self.client_node_sn, service['client_port_id'])

    def test_003_automated_from_in_construction_to_service_activated_error(self):
        push_service_to_orchestrator(self.service_id, "automated", "service_activated")
        service = get_service(self.service_id)
        self.assertEqual(service['service_state'], "bb_activation_in_progress")
        update_charles_service_state(self.service_id, "ERROR")
        service = get_service(self.service_id)
        self.assertEqual(service['service_state'], "ERROR")

    def test_004_hybrid_manual_till_bb_data_ack_then_automated(self):
        push_service_to_orchestrator(self.service_id, "manual", "bb_data_ack")
        service = get_service(self.service_id)
        self.assertEqual(service['service_state'], "bb_data_ack")
        
        push_service_to_orchestrator(self.service_id, "automated", "service_activated")
        service = get_service(self.service_id)
        self.assertEqual(service['service_state'], "bb_activation_in_progress")

        update_charles_service_state(self.service_id, "COMPLETED")
        service = get_service(self.service_id)
        self.assertEqual(service['service_state'], "cpe_activation_in_progress")

        update_charles_service_state(self.service_id, "COMPLETED")
        service = get_service(self.service_id)
        self.assertEqual(service['service_state'], "service_activated")

        #release client node port for further tests
        release_client_node_port(self.client_node_sn, service['client_port_id'])

    def test_005_manual_till_an_activated(self):
        push_service_to_orchestrator(self.service_id, "manual", "an_data_ack")
        service = get_service(self.service_id)
        self.assertEqual(service['service_state'], "an_data_ack")
        push_service_to_orchestrator(self.service_id, "manual", "an_activated")
        service = get_service(self.service_id)
        self.assertEqual(service['service_state'], "an_activated")

    def test_006_automated_till_an_activated(self):
        push_service_to_orchestrator(self.service_id, "automated", "an_activated")
        service = get_service(self.service_id)
        self.assertEqual(service['service_state'], "an_activation_in_progress")
        update_charles_service_state(self.service_id, "COMPLETED")
        service = get_service(self.service_id)
        self.assertEqual(service['service_state'], "an_activated")





@unittest.skip("testing irs")
class TestCpeMplsManualServiceMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        #create client
        create_client("test_client_03")
        cls.client_id = get_client_by_name("test_client_03")['id']
        cls.client_node_sn = "CCCC3333CCCC"
        cls.location = "LAB"

        #create customer location
        cls.customer_location_id = create_customer_location(cls.client_id)['id']

        #define service data
        cls.service_data =  {
                            "client": "test_client_03",
                            "bandwidth": 10,
                            "location": cls.location,
                            "customer_location_id": cls.customer_location_id
                            }

        cls.cpe_mpls_manual_service_id = "SVC01-Manual"
        cls.service_data['client_node_sn'] = cls.client_node_sn
        create_mock_service("cpe_mpls", cls.cpe_mpls_manual_service_id, cls.service_data )



    @classmethod
    def tearDownClass(cls):
        service = get_service(cls.cpe_mpls_manual_service_id)

        #free access port
        release_access_port(service['access_port_id'])

        #delete customer location
        delete_customer_location(cls.client_id, cls.customer_location_id)

        #delete client
        delete_client(cls.client_id)

        # print("jean grey services: ", get_services())
        # print("charles services: ", get_charles_services())

        #delete service at charles & JeanGrey
        delete_charles_service(cls.cpe_mpls_manual_service_id)


    def test_001_initial_service_state(self):      
        service_manual = get_service(self.cpe_mpls_manual_service_id)
        self.assertEqual(service_manual['service_state'], "in_construction")


    def test_002_manual_from_in_construction_to_bb_data_ack(self):
        push_service_to_orchestrator(self.cpe_mpls_manual_service_id, "manual", "bb_data_ack")
        service = get_service(self.cpe_mpls_manual_service_id)
        self.assertEqual(service['service_state'], "bb_data_ack")

    def test_003_manual_from_bb_data_ack_to_bb_activated(self):
        push_service_to_orchestrator(self.cpe_mpls_manual_service_id, "manual", "bb_activated")
        service = get_service(self.cpe_mpls_manual_service_id)
        self.assertEqual(service['service_state'], "bb_activated")

    def test_004_manual_from_bb_activated_to_cpe_data_ack(self):
        push_service_to_orchestrator(self.cpe_mpls_manual_service_id, "manual", "cpe_data_ack")
        service = get_service(self.cpe_mpls_manual_service_id)
        self.assertEqual(service['service_state'], "cpe_data_ack")

    def test_005_manual_from_cpe_data_ack_to_service_activated(self):
        push_service_to_orchestrator(self.cpe_mpls_manual_service_id, "manual", "service_activated")
        service = get_service(self.cpe_mpls_manual_service_id)
        self.assertEqual(service['service_state'], "service_activated")





class TestCpeIrsAutomatedServiceMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        #create client
        create_client("test_client")
        cls.client_id = get_client_by_name("test_client")['id']
        cls.client_node_sn = "CCCC3333CCCC"
        cls.access_node_id = 1
        cls.router_node_id = 1
        cls.location = "LAB"
        cls.initial_id = 1

        #create customer location
        cls.customer_location_id = create_customer_location(cls.client_id)['id']


    def setUp(self):
        #create VLAN
        data = {"vlan_tag":"3100"}
        self.vlan_tag = create_vlan_tag(data)
        print(self.vlan_tag)

        #add VLAN to access_node
        data = {"vlan_id":self.vlan_tag["id"]}
        add_vlan_to_access_node(self.access_node_id,data)

        #create LogicalUnit
        data = {"logical_unit_id":15000}
        self.lu = create_logicalunit(data)

        #add LU to routerNode
        add_logical_unit_to_router_node(self.router_node_id,self.lu["id"])

        #create access_port
        data = {"used" : "False", "port" : "GigabitEthernet 1/19"}
        self.access_port = create_access_port_at_access_node(self.access_node_id, data)

        #create client node port
        data = {"interface_name":"GigabitEthernet 1/1", "used" : "False", "service_id" : ""}
        self.client_node_port = create_client_port_at_client_node(self.client_node_sn, data)

        #define service data
        self.service_data =  {
                            "client": "test_client_03",
                            "bandwidth": 10,
                            "location": self.location,
                            "customer_location_id": self.customer_location_id,
                            "prefix": 29
                            }

        self.service_id = "SVC01-A_" + str(self.initial_id)
        self.service_data['client_node_sn'] = self.client_node_sn
        
        #create mock service
        create_mock_service("cpe_irs", self.service_id, self.service_data )



    def tearDown(self):
        service = get_service(self.service_id)

        #free access port
        release_access_port(service['access_port_id'])
        
        #delete VLAN
        delete_vlan_tag(self.vlan_tag["id"])

        #delete LogicalUnit
        delete_logicalunit(self.lu["id"])

        #delete access_port
        delete_access_port(self.access_port["id"])

        #delete client_port
        delete_client_port(self.client_node_port)

        #delete service at charles & JeanGrey
        delete_charles_service(self.service_id)
        delete_jeangrey_service(self.service_id)
        self.__class__.initial_id = self.__class__.initial_id + 1



    @classmethod
    def tearDownClass(cls):
        #delete client
        delete_client(cls.client_id)

        #delete customer location
        delete_customer_location(cls.client_id, cls.customer_location_id)

    def test_001_initial_service_state(self):      
        service_manual = get_service(self.service_id)
        self.assertEqual(service_manual['service_state'], "in_construction")

    # def test_002_automated_from_in_construction_to_service_activated_ok(self):
    #     push_service_to_orchestrator(self.service_id, "automated", "service_activated")
        
    #     service = get_service(self.service_id)
    #     self.assertEqual(service['service_state'], "an_activation_in_progress")
    #     try:
    #         update_charles_service_state(self.service_id, "COMPLETED")
    #     except BaseException as e:
    #         service = get_service(self.service_id)
    #         print(service['service_state'])

    #     service = get_service(self.service_id)
    #     self.assertEqual(service['service_state'], "bb_activation_in_progress")
    #     update_charles_service_state(self.service_id, "COMPLETED")

    #     service = get_service(self.service_id)
    #     self.assertEqual(service['service_state'], "cpe_activation_in_progress")
    #     update_charles_service_state(self.service_id, "COMPLETED")

    #     service = get_service(self.service_id)
    #     self.assertEqual(service['service_state'], "service_activated")
        
    #     #release client node port for further tests
    #     release_client_node_port(self.client_node_sn, service['client_port_id'])

    # def test_003_automated_from_in_construction_to_service_activated_error(self):
    #     push_service_to_orchestrator(self.service_id, "automated", "service_activated")
    #     service = get_service(self.service_id)
    #     self.assertEqual(service['service_state'], "an_activation_in_progress")
    #     update_charles_service_state(self.service_id, "ERROR")
    #     service = get_service(self.service_id)
    #     self.assertEqual(service['service_state'], "ERROR")

    # def test_004_hybrid_manual_till_an_data_ack_then_automated(self):
    #     push_service_to_orchestrator(self.service_id, "manual", "an_data_ack")
    #     service = get_service(self.service_id)
    #     self.assertEqual(service['service_state'], "an_data_ack")
        
    #     push_service_to_orchestrator(self.service_id, "automated", "service_activated")
        
    #     service = get_service(self.service_id)
    #     self.assertEqual(service['service_state'], "an_activation_in_progress")
    #     update_charles_service_state(self.service_id, "COMPLETED")

    #     service = get_service(self.service_id)
    #     self.assertEqual(service['service_state'], "bb_activation_in_progress")
    #     update_charles_service_state(self.service_id, "COMPLETED")

    #     service = get_service(self.service_id)
    #     self.assertEqual(service['service_state'], "cpe_activation_in_progress")
    #     update_charles_service_state(self.service_id, "COMPLETED")
        
    #     service = get_service(self.service_id)
    #     self.assertEqual(service['service_state'], "service_activated")

    #     #release client node port for further tests
    #     release_client_node_port(self.client_node_sn, service['client_port_id'])

    # def test_005_manual_till_an_activated(self):
    #     push_service_to_orchestrator(self.service_id, "manual", "an_data_ack")
    #     service = get_service(self.service_id)
    #     self.assertEqual(service['service_state'], "an_data_ack")
    #     push_service_to_orchestrator(self.service_id, "manual", "an_activated")
    #     service = get_service(self.service_id)
    #     self.assertEqual(service['service_state'], "an_activated")

    # def test_006_automated_till_an_activated(self):
    #     push_service_to_orchestrator(self.service_id, "automated", "an_activated")
    #     service = get_service(self.service_id)
    #     self.assertEqual(service['service_state'], "an_activation_in_progress")
    #     update_charles_service_state(self.service_id, "COMPLETED")
    #     service = get_service(self.service_id)
    #     self.assertEqual(service['service_state'], "an_activated")




















@unittest.skip("testing irs")
class TestCpeIrsManualServiceMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        #create client
        create_client("test_client_03")
        cls.client_id = get_client_by_name("test_client_03")['id']
        cls.client_node_sn = "CCCC3333CCCC"
        cls.location = "LAB"

        #create customer location
        cls.customer_location_id = create_customer_location(cls.client_id)['id']

        #define service data
        cls.service_data =  {
                            "client": "test_client_03",
                            "bandwidth": 10,
                            "location": cls.location,
                            "customer_location_id": cls.customer_location_id,
                            "prefix": 29
                            }

        cls.cpe_mpls_manual_service_id = "SVC01-Manual"
        cls.service_data['client_node_sn'] = cls.client_node_sn
        create_mock_service("cpe_irs", cls.cpe_mpls_manual_service_id, cls.service_data )



    @classmethod
    def tearDownClass(cls):
        service = get_service(cls.cpe_mpls_manual_service_id)

        #free access port
        release_access_port(service['access_port_id'])

        #delete customer location
        delete_customer_location(cls.client_id, cls.customer_location_id)

        #delete client
        delete_client(cls.client_id)


        # print("jean grey services: ", get_services())
        # print("charles services: ", get_charles_services())

        #delete service at charles & JeanGrey
        delete_charles_service(cls.cpe_mpls_manual_service_id)


    def test_001_initial_service_state(self):      
        service_manual = get_service(self.cpe_mpls_manual_service_id)
        self.assertEqual(service_manual['service_state'], "in_construction")

    def test_002_manual_from_in_construction_to_an_data_ack(self):
        push_service_to_orchestrator(self.cpe_mpls_manual_service_id, "manual", "an_data_ack")
        service = get_service(self.cpe_mpls_manual_service_id)
        self.assertEqual(service['service_state'], "an_data_ack")

    def test_003_manual_from_bb_data_ack_to_an_activated(self):
        push_service_to_orchestrator(self.cpe_mpls_manual_service_id, "manual", "an_activated")
        service = get_service(self.cpe_mpls_manual_service_id)
        self.assertEqual(service['service_state'], "an_activated")


    def test_004_manual_from_in_construction_to_bb_data_ack(self):
        push_service_to_orchestrator(self.cpe_mpls_manual_service_id, "manual", "bb_data_ack")
        service = get_service(self.cpe_mpls_manual_service_id)
        self.assertEqual(service['service_state'], "bb_data_ack")

    def test_005_manual_from_bb_data_ack_to_bb_activated(self):
        push_service_to_orchestrator(self.cpe_mpls_manual_service_id, "manual", "bb_activated")
        service = get_service(self.cpe_mpls_manual_service_id)
        self.assertEqual(service['service_state'], "bb_activated")

    def test_006_manual_from_bb_activated_to_cpe_data_ack(self):
        push_service_to_orchestrator(self.cpe_mpls_manual_service_id, "manual", "cpe_data_ack")
        service = get_service(self.cpe_mpls_manual_service_id)
        self.assertEqual(service['service_state'], "cpe_data_ack")

    def test_007_manual_from_cpe_data_ack_to_service_activated(self):
        push_service_to_orchestrator(self.cpe_mpls_manual_service_id, "manual", "service_activated")
        service = get_service(self.cpe_mpls_manual_service_id)
        self.assertEqual(service['service_state'], "service_activated")












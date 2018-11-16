# from django.test import SimpleTestCase, LiveServerTestCase
import unittest

from charles.models import Service
from charles.utils.fsm import Fsm
from charles.utils.utils import *


def create_mock_service(service_type, service_id, data):
    data['service_type'] = service_type
    data['id'] = service_id
    create_core_service(data)



class TestCpeMplsServiceMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        #create client
        create_client("test_client")
        cls.client_id = get_client_by_name("test_client")['id']
        cls.client_node_sn = "CCCC3333CCCC"
        cls.location = "LAB"

        #create customer location
        cls.customer_location_id = create_customer_location(cls.client_id)['id']

        #define service data
        cls.service_data =  {
                            "client": "test_client",
                            "bandwidth": 10,
                            "location": cls.location,
                            "customer_location_id": cls.customer_location_id
                            }

        cls.cpe_mpls_manual_service_id = "SVC01-Manual"
        cls.cpe_mpls_automated_service_id = "SVC01-Automated"
        cls.cpe_mpls_automated_error_service_id = "SVC01-Automated-error"
        cls.cpe_mpls_hybrid_service_id = "SVC01-Automated-hybrid"
        cls.cpeless_irs_service_id = "SVC02"
        cls.vpls_service_id = "SVC03"
        cls.cpeless_mpls_service_id = "SVC04"
        cls.cpe_mpls_an_data_service_id = "SVC01-AN_data"
        cls.cpe_mpls_an_auto_service_id = "SVC01-AN_auto"
        

        # create_mock_service("cpeless_irs_service_id", cls.cpeless_irs_service_id, data )
        # create_mock_service("cpeless_mpls_service_id", cls.cpeless_mpls_service_id, data )

        cls.service_data['client_node_sn'] = cls.client_node_sn
        #create_mock_service("vpls_service_id", cls.vpls_service_id, data )
        create_mock_service("cpe_mpls", cls.cpe_mpls_manual_service_id, cls.service_data )
        create_mock_service("cpe_mpls", cls.cpe_mpls_automated_service_id, cls.service_data )
        create_mock_service("cpe_mpls", cls.cpe_mpls_automated_error_service_id, cls.service_data )
        create_mock_service("cpe_mpls", cls.cpe_mpls_hybrid_service_id, cls.service_data )
        create_mock_service("cpe_mpls", cls.cpe_mpls_an_data_service_id, cls.service_data )
        create_mock_service("cpe_mpls", cls.cpe_mpls_an_auto_service_id, cls.service_data )


    @classmethod
    def tearDownClass(cls):

        service = get_service(cls.cpe_mpls_manual_service_id)
        service_auto = get_service(cls.cpe_mpls_automated_service_id)
        service_auto_error = get_service(cls.cpe_mpls_automated_error_service_id)
        service_auto_hybrid = get_service(cls.cpe_mpls_hybrid_service_id)
        service_an_data = get_service(cls.cpe_mpls_an_data_service_id)
        service_an_auto = get_service(cls.cpe_mpls_an_auto_service_id)

        #free access port
        release_access_port(service['access_port_id'])
        release_access_port(service_auto['access_port_id'])
        release_access_port(service_auto_error['access_port_id'])
        release_access_port(service_auto_hybrid['access_port_id'])
        release_access_port(service_an_data['access_port_id'])
        release_access_port(service_an_auto['access_port_id'])


        #delete client
        delete_client(cls.client_id)
        # print("clients: ",get_clients() )
        # print("customer locations: ",get_customer_locations(cls.client_id) )

        #delete customer location
        delete_customer_location(cls.client_id, cls.customer_location_id)

        print("jean grey services: ", get_services())
        print("charles services: ", get_charles_services())

        #delete service at charles & JeanGrey
        delete_charles_service(cls.cpe_mpls_manual_service_id)
        delete_charles_service(cls.cpe_mpls_automated_service_id)
        delete_charles_service(cls.cpe_mpls_automated_error_service_id)
        delete_charles_service(cls.cpe_mpls_hybrid_service_id)
        delete_charles_service(cls.cpe_mpls_an_data_service_id)
        delete_charles_service(cls.cpe_mpls_an_auto_service_id)


    def test_001_initial_service_state(self):      
        service_manual = get_service(self.cpe_mpls_manual_service_id)
        service_automated = get_service(self.cpe_mpls_automated_service_id)
        service_automated_error = get_service(self.cpe_mpls_automated_error_service_id)
        service_hybrid = get_service(self.cpe_mpls_hybrid_service_id)
        # print(service)
        self.assertEqual(service_manual['service_state'], "IN_CONSTRUCTION")
        self.assertEqual(service_automated['service_state'], "IN_CONSTRUCTION")
        self.assertEqual(service_automated_error['service_state'], "IN_CONSTRUCTION")
        self.assertEqual(service_hybrid['service_state'], "IN_CONSTRUCTION")

    def test_next_state(self):
        pass

    def test_automated(self):
        pass

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

    def test_006_automated_from_in_construction_to_service_activated_ok(self):
        push_service_to_orchestrator(self.cpe_mpls_automated_service_id, "automated", "service_activated")
        service = get_service(self.cpe_mpls_automated_service_id)
        self.assertEqual(service['service_state'], "BB_ACTIVATION_IN_PROGRESS")
        update_charles_service_state(self.cpe_mpls_automated_service_id, "COMPLETED")
        service = get_service(self.cpe_mpls_automated_service_id)
        self.assertEqual(service['service_state'], "CPE_ACTIVATION_IN_PROGRESS")
        update_charles_service_state(self.cpe_mpls_automated_service_id, "COMPLETED")
        service = get_service(self.cpe_mpls_automated_service_id)
        self.assertEqual(service['service_state'], "service_activated")

    def test_007_automated_from_in_construction_to_service_activated_error(self):
        push_service_to_orchestrator(self.cpe_mpls_automated_error_service_id, "automated", "service_activated")
        service = get_service(self.cpe_mpls_automated_error_service_id)
        self.assertEqual(service['service_state'], "BB_ACTIVATION_IN_PROGRESS")
        update_charles_service_state(self.cpe_mpls_automated_error_service_id, "ERROR")
        service = get_service(self.cpe_mpls_automated_error_service_id)
        self.assertEqual(service['service_state'], "error")

    def test_008_hybrid_manual_till_bb_data_ack_then_automated(self):
        push_service_to_orchestrator(self.cpe_mpls_hybrid_service_id, "manual", "bb_data_ack")
        service = get_service(self.cpe_mpls_hybrid_service_id)
        self.assertEqual(service['service_state'], "bb_data_ack")
        
        push_service_to_orchestrator(self.cpe_mpls_hybrid_service_id, "automated", "service_activated")
        service = get_service(self.cpe_mpls_hybrid_service_id)
        self.assertEqual(service['service_state'], "BB_ACTIVATION_IN_PROGRESS")

        update_charles_service_state(self.cpe_mpls_hybrid_service_id, "COMPLETED")
        service = get_service(self.cpe_mpls_hybrid_service_id)
        self.assertEqual(service['service_state'], "CPE_ACTIVATION_IN_PROGRESS")

        update_charles_service_state(self.cpe_mpls_hybrid_service_id, "COMPLETED")
        service = get_service(self.cpe_mpls_hybrid_service_id)
        self.assertEqual(service['service_state'], "service_activated")

    def test_009_manual_till_an_activated(self):
        push_service_to_orchestrator(self.cpe_mpls_automated_service_id, "automated", "service_activated")
        service = get_service(self.cpe_mpls_automated_service_id)
        self.assertEqual(service['service_state'], "BB_ACTIVATION_IN_PROGRESS")
        update_charles_service_state(self.cpe_mpls_automated_service_id, "COMPLETED")
        service = get_service(self.cpe_mpls_automated_service_id)
        self.assertEqual(service['service_state'], "CPE_ACTIVATION_IN_PROGRESS")
        update_charles_service_state(self.cpe_mpls_automated_service_id, "COMPLETED")
        service = get_service(self.cpe_mpls_automated_service_id)
        self.assertEqual(service['service_state'], "service_activated")


    def test_worker_response(self):
        pass






# from django.test import SimpleTestCase, LiveServerTestCase
import unittest

from charles.models import Service
from charles.utils.fsm import Fsm
from charles.utils.utils import *


def create_mock_service(service_type, service_id, data):
    data['service_type'] = service_type
    create_core_service(cls.service_data)



class TestServiceMethods(unittest.TestCase):

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
                            "id": service_id,
                            "customer_location_id": cls.customer_location_id
                            }

        cls.cpe_mpls_service_id = "SVC01"
        cls.cpeless_irs_service_id = "SVC02"
        cls.vpls_service_id = "SVC03"
        cls.cpeless_mpls_service_id = "SVC04"
        

        # create_mock_service("cpeless_irs_service_id", cls.cpeless_irs_service_id, data )
        # create_mock_service("cpeless_mpls_service_id", cls.cpeless_mpls_service_id, data )

        data['client_node_sn'] = cls.client_node_sn
        # create_mock_service("vpls_service_id", cls.vpls_service_id, data )
        create_mock_service("cpe_mpls", cls.cpe_mpls_service_id, data )



    @classmethod
    def tearDownClass(cls):
        #delete client
        delete_client(cls.client_id)

        #delete customer location
        delete_customer_location(cls.client_id, cls.customer_location_id)



    def test_initial_service_state(self):


        # r = get_customer_location(client_id, customer_location_id)
        print(self.client_id)
        print(self.customer_location_id)
        self.assertTrue(True)

    def test_next_state(self):
        pass

    def test_automated(self):
        pass


    def test_worker_response(self):
        pass






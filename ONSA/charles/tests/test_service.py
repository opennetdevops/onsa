from django.test import TestCase
from charles.models import Service
from charles.utils.fsm import Fsm
from charles.utils.utils import *

class TestServiceMethods(TestCase):


    @classmethod
    def setUpClass(cls):
        create_client("test_client")
        cls.client_id = get_client_by_name("test_client")['id']


        #create customer location

        #
        # create_customer_location(client_id)

    @classmethod
    def tearDownClass(cls):
        delete_client(cls.client_id)

    def test_initial_service_state(self):


        # r = get_customer_location(client_id, customer_location_id)
        print(self.client_id)
        self.assertTrue(True)

    def test_next_state(self):
        pass

    def test_automated(self):
        pass


    def test_worker_response(self):
        pass






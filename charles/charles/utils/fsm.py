from charles.services import cpeless_irs_service, cpe_mpls_service, cpeless_mpls_service, vcpe_irs_service, cpe_irs_service
from charles.services import vpls_service
from enum import Enum
from charles.utils.utils import *

import logging
import coloredlogs

coloredlogs.install(level='DEBUG')
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


class ServiceTypes(Enum):
    cpeless_irs = cpeless_irs_service
    cpe_mpls = cpe_mpls_service
    cpeless_mpls = cpeless_mpls_service
    vcpe_irs = vcpe_irs_service
    cpe_irs = cpe_irs_service
    vpls = vpls_service


##
## IN_CONS. -> AN_DATA -> AN_ACT_IN_PROG -> AN_ACT -> BB_DATA -> BB_ACT_IN_PROG -> BB_ACT -> CPE_DATA_ACK
##
NextStateMap = (    
                    #From IN_CONSTRUNCTION
                    {'src':"in_construction",
                    'dst': "an_activated",
                    'next_state':"an_data_ack" },
                    {'src':"in_construction",
                    'dst': "an_data_ack",
                    'next_state':"an_data_ack" },
                    {'src':"in_construction",
                    'dst': "cpe_data_ack",
                    'next_state':"an_data_ack" },
                    {'src':"in_construction",
                    'dst': "bb_data_ack",
                    'next_state':"an_data_ack" },
                    {'src':"in_construction",
                    'dst': "service_activated",
                    'next_state':"an_data_ack" },

                    #From an_data_ack
                    {'src':"an_data_ack",
                    'dst': "an_activated",
                    'next_state':"an_activated" },
                    {'src':"an_data_ack",
                    'dst': "bb_activated",
                    'next_state':"an_activated" },
                    {'src':"an_data_ack",
                    'dst': "cpe_data_ack",
                    'next_state':"an_activated" },
                    {'src':"an_data_ack",
                    'dst': "service_activated",
                    'next_state':"an_activated" },

                    #From an_activation_in_progress
                    {'src':"an_activation_in_progress",
                    'dst': "an_activated",
                    'next_state':"an_activated" },
                    {'src':"an_activation_in_progress",
                    'dst': "service_activated",
                    'next_state':"an_activated" },
                     {'src':"an_activation_in_progress",
                    'dst': "cpe_data_ack",
                    'next_state':"an_activated" },

                    #From an_activated
                    {'src':"an_activated",
                    'dst': "bb_data_ack",
                    'next_state':"bb_data_ack" },
                    {'src':"an_activated",
                    'dst': "cpe_data_ack",
                    'next_state':"bb_data_ack" },
                    {'src':"an_activated",
                    'dst': "service_activated",
                    'next_state':"bb_data_ack" },
                    {'src':"an_activated",
                    'dst': "bb_activated",
                    'next_state':"bb_data_ack" },


                    #From bb_data_ack
                    {'src':"bb_data_ack",
                    'dst': "bb_activated",
                    'next_state':"bb_activated" },
                    {'src':"bb_data_ack",
                    'dst': "service_activated",
                    'next_state':"bb_activated" },
                    {'src':"bb_data_ack",
                    'dst': "cpe_data_ack",
                    'next_state':"bb_activated" },

                    # From bb_activation_in_progress
                    {'src':"bb_activation_in_progress",
                    'dst': "bb_activated",
                    'next_state':"bb_activated" },
                    {'src':"bb_activation_in_progress",
                    'dst': "cpe_data_ack",
                    'next_state':"bb_activated" },
                    {'src':"bb_activation_in_progress",
                    'dst': "service_activated",
                    'next_state':"bb_activated" },

                    #From bb_activated
                    {'src':"bb_activated",
                    'dst': "cpe_data_ack",
                    'next_state':"cpe_data_ack" },
                    {'src':"bb_activated",
                    'dst': "service_activated",
                    'next_state':"cpe_data_ack" },

                    #From cpe_activation_in_progress
                    {'src':"cpe_activation_in_progress",
                    'dst': "service_activated",
                    'next_state':"service_activated" },
                    
                    #From cpe_data_ack
                    {'src':"cpe_data_ack",
                    'dst': "service_activated",
                    'next_state':"service_activated" }
                )

def next_state(source_state,target_state):
    for state in NextStateMap:
        if state['src'] == source_state and state['dst'] == target_state:
            return state['next_state']


class Fsm():
    def run(service):
        state = next_state(service['service_state'], service['target_state'])
        logging.debug(state)
        generate_request = getattr(StateTypes[state].value, "do_" + service['deployment_mode'])
        service_data = generate_request(service)

        if service_data['service_state'] is not "error":
            #update charles, JG will be updated from the main service view
            charles_service = Service.objects.get(service_id=service_data['service_id'])
            charles_service.last_state = charles_service.service_state
            charles_service.service_state = service_data['service_state']
            charles_service.save()

            #While current_state != target_state keep working
            if service_data['service_state'] != service['target_state']:
                state = next_state(service_data['service_state'], service['target_state'])
                generate_request = getattr(StateTypes[state].value, "do_" + service['deployment_mode'])
                service_data = generate_request(service)
            return service_data['service_state']
        return None

    def to_next_state(service):
        state = next_state(service['service_state'], service['target_state'])
        generate_request = getattr(StateTypes[state].value, "do_manual")
        return generate_request(service)
        


class State():
    def do_automated(service):
        print("not implemented")
        return

class bb_data_ack(State):
    def do_manual(service):
        #TODO ESTO SE HACE POR REFLECTION FACIL
        return "bb_data_ack"

    def do_automated(service):
        generate_request = getattr(ServiceTypes[service['service_type']].value, "bb_data_ack_" + service['deployment_mode'] + "_request")
        return  generate_request(service)

class bb_activated(State):
    def do_manual(service):
        #TODO ESTO SE HACE POR REFLECTION FACIL
        return "bb_activated"

    def do_automated(service):
        generate_request = getattr(ServiceTypes[service['service_type']].value, "bb_activated_" + service['deployment_mode'] + "_request")
        return  generate_request(service)

class an_data_ack(State):
    def do_manual(service):
        #TODO ESTO SE HACE POR REFLECTION FACIL
        return "an_data_ack"

    def do_automated(service):
        generate_request = getattr(ServiceTypes[service['service_type']].value, "an_data_ack_" + service['deployment_mode'] + "_request")
        return  generate_request(service)

class an_activated(State):
    def do_manual(service):
        #TODO ESTO SE HACE POR REFLECTION FACIL
        return "an_activated"

    def do_automated(service):
        generate_request = getattr(ServiceTypes[service['service_type']].value, "an_activated_" + service['deployment_mode'] + "_request")
        return  generate_request(service)

class cpe_data_ack(State):
    def do_manual(service):
        #TODO ESTO SE HACE POR REFLECTION FACIL
        return "cpe_data_ack"

    def do_automated(service):
        generate_request = getattr(ServiceTypes[service['service_type']].value, "cpe_data_ack_" + service['deployment_mode'] + "_request")
        return  generate_request(service)

class service_activated(State):
    def do_manual(service):
        #TODO ESTO SE HACE POR REFLECTION FACIL
        return "service_activated"

    def do_automated(service):
        generate_request = getattr(ServiceTypes[service['service_type']].value, "service_activated_" + service['deployment_mode'] + "_request")
        return  generate_request(service)

class bb_activation_in_progress(State):
    def do_manual(service):
        #TODO ESTO SE HACE POR REFLECTION FACIL
        return "bb_activation_in_progress"

class cpe_activation_in_progress(State):
    def do_manual(service):
        #TODO ESTO SE HACE POR REFLECTION FACIL
        return "cpe_activation_in_progress"

class an_activation_in_progress(State):
    def do_manual(service):
        #TODO ESTO SE HACE POR REFLECTION FACIL
        return "cpe_activation_in_progress"

class StateTypes(Enum):
    # Access node states
    an_data_ack = an_data_ack
    an_activation_in_progress = an_activation_in_progress
    an_activated = an_activated

    # Backbone states
    bb_data_ack = bb_data_ack
    bb_activation_in_progress = bb_activation_in_progress
    bb_activated = bb_activated

    # CPE states
    cpe_data_ack = cpe_data_ack
    cpe_activation_in_progress = cpe_activation_in_progress
    service_activated = service_activated


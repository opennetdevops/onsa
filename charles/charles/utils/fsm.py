from charles.services import cpeless_irs_service, cpe_mpls_service, cpeless_mpls_service, vcpe_irs_service, cpe_irs_service
from charles.services import vpls_service
from charles.models import *
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
                    {'src':"an_data_ack",
                    'dst': "bb_data_ack",
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
        try:
            #Search next state in FSM MAP
            logging.debug(str("from service: "+service['service_state'] +" to: "+ service['target_state']))
            
            state = State(next_state(service['service_state'], service['target_state']))
            logging.debug(str("proposed next state " + state.name))
            
            result_state = state.run(service)

            while result_state != "error" and keep_processing(result_state) and result_state != service['target_state']:
                #update charles, JG will be updated from the main service view
                service = update_charles_service(service, result_state)

                #Execute next step
                state.name = next_state(result_state, service['target_state'])
                logging.debug(str("running " +state.name))
                result_state = state.run(service)
            
            return result_state
        
        except Service.DoesNotExist as msg:
            logging.error(msg)
            raise ServiceException("Invalid Service")

    #Manually return next state name
    def to_next_state(service):
        state = State(next_state(service['service_state'], service['target_state']))
        return state.do_manual()



def update_charles_service(service, state):
    charles_service = Service.objects.get(service_id=service['service_id'])
    charles_service.last_state = charles_service.service_state
    charles_service.service_state = state
    charles_service.save()
    return charles_service.fields()

def keep_processing(state):
    # logging.debug(state)
    if "in_progress" in state:
        return False
    return True




class State():

    name = None

    def __init__(self,name):
        self.name = name

    def run(self,service):
        # logging.debug(service)
        # logging.debug(service['deployment_mode'])
        if service['deployment_mode'] == "manual":
            return self.do_manual()
        return self.do_automated(service)


    def do_manual(self):
        return self.name

    def do_automated(self, service):  
        generate_request = getattr(ServiceTypes[service['service_type']].value, self.name+ "_" + service['deployment_mode'] + "_request")
        return generate_request(service)


# class bb_data_ack(State):
#     pass

# class bb_activated(State):
#     pass

# class an_data_ack(State):
#     pass

# class an_activated(State):
#     pass

# class cpe_data_ack(State):
#     pass

# class service_activated(State):
#     pass

# class bb_activation_in_progress(State):
#     pass

# class cpe_activation_in_progress(State):
#     pass

# class an_activation_in_progress(State):
#     pass


# class StateTypes(Enum):
#     # Access node states
#     an_data_ack = an_data_ack
#     an_activation_in_progress = an_activation_in_progress
#     an_activated = an_activated

#     # Backbone states
#     bb_data_ack = bb_data_ack
#     bb_activation_in_progress = bb_activation_in_progress
#     bb_activated = bb_activated

#     # CPE states
#     cpe_data_ack = cpe_data_ack
#     cpe_activation_in_progress = cpe_activation_in_progress
#     service_activated = service_activated


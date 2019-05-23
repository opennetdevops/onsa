from charles.services import cpeless_irs_service, cpe_mpls_service, cpeless_mpls_service, vcpe_irs_service, cpe_irs_service
from charles.services import vpls_service
from charles.models import *
from enum import Enum
from charles.utils.utils import *
from charles.utils.inventory_utils import *
from charles.utils.ipam_utils import *

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
## IN_CONS. -> AN_ACT_IN_PROG -> AN_ACT -> BB_DATA -> BB_ACT_IN_PROG -> BB_ACT -> CPE_DATA_ACK
##
NextStateMap = (    
                    #From IN_CONSTRUNCTION
                    {'src':"in_construction",
                    'dst': "an_activated",
                    'next_state':"an_activated" },
                    {'src':"in_construction",
                    'dst': "cpe_data_ack",
                    'next_state':"an_activated" },
                    {'src':"in_construction",
                    'dst': "bb_data_ack",
                    'next_state':"an_activated" },
                    {'src':"in_construction",
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
        try:
            #Search next state in FSM MAP
            logging.debug(str("from service: "+service['service_state'] +" to: "+ service['target_state']))
            
            state = State(next_state(service['service_state'], service['target_state']))
            logging.debug(str("proposed next state " + state.name))
            service = state.run(service)
            logging.debug(str("Service after run:" + str(service)))
            print(service)


            while service['service_state'] != "error" and keep_processing(service['service_state']) and service['service_state'] != service['target_state']:
                #Execute next step
                logging.debug(str("from service: "+service['service_state'] +" to: "+ service['target_state']))
                state.name = next_state(service['service_state'], service['target_state'])
                logging.debug(str("running " +state.name))
                service = state.run(service)
                logging.debug(str("Service after inner while run:" + str(service)))
            
            return service['service_state']
        
        except Service.DoesNotExist as msg:
            logging.error(msg)
            raise ServiceException("Invalid Service")

    #Manually return next state name
    def to_next_state(service):
        state = State(next_state(service['service_state'], service['target_state']))
        return state.do_manual(service)



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
            return self.do_manual(service)
        return self.do_automated(service)

    def do_manual(self, service):
        logging.debug("Manual")
        service['service_state'] = self.name
        service_data = {'service_state': self.name}
        update_jeangrey_service(service['service_id'], service_data)
        service = update_charles_service(service, self.name)
        return service

    def do_automated(self, service):  
        generate_request = getattr(ServiceTypes[service['service_type']].value, self.name+ "_" + service['deployment_mode'] + "_request")
        return generate_request(service)


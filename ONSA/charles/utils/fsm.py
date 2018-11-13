from charles.services import cpeless_irs_service, cpe_mpls_service, cpeless_mpls_service, vcpe_irs_service
from charles.services import vpls_service
from enum import Enum



class ServiceTypes(Enum):
    cpeless_irs = cpeless_irs_service
    cpe_mpls = cpe_mpls_service
    cpeless_mpls = cpeless_mpls_service
    vcpe_irs = vcpe_irs_service
    vpls = vpls_service


NextStateMap = (    {'src':"IN_CONSTRUCTION",
                    'dst': "bb_activated",
                    'next_state':"bb_data_ack" },
                    {'src':"IN_CONSTRUCTION",
                    'dst': "bb_data_ack",
                    'next_state':"bb_data_ack" },
                    {'src':"IN_CONSTRUCTION",
                    'dst': "service_activated",
                    'next_state':"bb_data_ack" },
                    {'src':"IN_CONSTRUCTION",
                    'dst': "an_activated",
                    'next_state':"an_data_ack" },
                    {'src':"IN_CONSTRUCTION",
                    'dst': "an_data_ack",
                    'next_state':"an_data_ack" },
                    {'src':"bb_data_ack",
                    'dst': "bb_activated",
                    'next_state':"bb_activated" },
                    {'src':"bb_data_ack",
                    'dst': "service_activated",
                    'next_state':"bb_activated" },
                    {'src':"bb_activated",
                    'dst': "service_activated",
                    'next_state':"cpe_data_ack" },
                    {'src':"cpe_data_ack",
                    'dst': "service_activated",
                    'next_state':"service_activated" },
                    {'src':"an_data_ack",
                    'dst': "an_activated",
                    'next_state':"an_activated" }
                )

def next_state(source_state,target_state):
    for state in NextStateMap:
        if state['src'] == source_state and state['dst'] == target_state:
            return state['next_state']


class Fsm():
    def run(service):
        state = next_state(service['service_state'], service['target_state'])
        generate_request = getattr(state, "do_" + service['deployment_mode'])
        req_state = generate_request(service)
        
        if req_state is not "error":
            if req_state != service['target_state']:
                state = next_state(req_state, service['target_state'])
                generate_request = getattr(state, "do_" + service['deployment_mode'])
                req_state = generate_request(service)
            return req_state
        return None 

    def to_next_state(service):
        state = next_state(service['service_state'], service['target_state'])
        generate_request = getattr(state, "do_manual")
        return generate_request(service)
        


class State():
    def do_automated(service):
        generate_request = getattr(ServiceTypes[service['service_type']].value, service['service_type'] + service['deployment_mode'] + "_request")
        return  generate_request(service)

class bb_data_ack(State):
    def do_manual(service):
        #TODO ESTO SE HACE POR REFLECTION FACIL
        print(type(self))
        return "bb_data_ack"
        
class bb_activated(State):
    def do_manual(service):
        #TODO ESTO SE HACE POR REFLECTION FACIL
        print(type(self))
        return "bb_activated"

class an_data_ack(State):
    def do_manual(service):
        #TODO ESTO SE HACE POR REFLECTION FACIL
        print(type(self))
        return "an_data_ack"

class an_activated(State):
    def do_manual(service):
        #TODO ESTO SE HACE POR REFLECTION FACIL
        print(type(self))
        return "an_activated"

class cpe_data_ack(State):
    def do_manual(service):
        #TODO ESTO SE HACE POR REFLECTION FACIL
        print(type(self))
        return "cpe_data_ack"

class service_activated(State):
    def do_manual(service):
        #TODO ESTO SE HACE POR REFLECTION FACIL
        print(type(self))
        return "service_activated"





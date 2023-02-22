from tmp_declaration import *
from structure import *

def type1Task():
    system_event_group.wait()
    bits_to_wait_for = initial_sanity_check_bit | runtime_sanity_check_bit
    while not (system_event_group.is_set() & bits_to_wait_for):
        system_event_group.wait()
    
    while(1):
        syncDateTime()


def idleTask():
    pass
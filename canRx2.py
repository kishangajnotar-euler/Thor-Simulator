from main import CAN_2 as bus
def can2():
    msg = bus.recv()
    while(msg): 
        print("CAN 2 ", msg)
        msg = bus.recv()   
import threading
from canRx1 import can1
from canRx2 import can2
can1Rx = None 
can2Rx = None


def createTasks():
    global can1Rx, can2Rx
    can1Rx = threading.Thread(target =can1)
    can2Rx = threading.Thread(target =can2)

def stask():
    can1Rx.start()
    can2Rx.start()

    



import threading
from threads import chargingStationMain
from threads import telemetryDevice 
from canRx1 import can1
from canRx2 import can2
can1Rx = None 
can2Rx = None
chargingStationSanityTask = None
chargerLoop = None
telemetryParser = None
type1Task = None
idleTask = None
ledTask = None
energyMeterTask = None
starkTXCallback = None


def createTasks():
    global can1Rx, can2Rx,type1Task,telemetryParser
    can1Rx = threading.Thread(target =can1)
    can2Rx = threading.Thread(target =can2)
    type1Task=threading.Thread(target=chargingStationMain.type1Task)
    telemetryParser=threading.Thread(target=telemetryDevice.telemetryParser)
def stask():
    can1Rx.start()
    can2Rx.start()
    chargingStationSanityTask.start()
    type1Task.start()
 

    



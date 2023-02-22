import threading
from threads import chargingStationTest
from threads import chargingStationMain
from threads import energyMeter
from threads import flashCharger
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
    global can1Rx, can2Rx
    can1Rx = threading.Thread(target =can1)
    can2Rx = threading.Thread(target =can2)
    chargingStationSanityTask=threading.Thread(target=chargingStationTest.chargingStationSanityTask,args=())
    chargerLoop=threading.Thread(target=chargingStationMain.chargerLoop,args=())
    telemetryParser=threading.Thread(target=telemetryDevice.telemetryParser,args=())
    # type1Task=threading.Thread(target=type1Task,args=())
    # idleTask=threading.Thread(target=idleTask,args=())
    # ledTask=threading.Thread(target=ledTask,args=())
    energyMeterTask=threading.Thread(target=energyMeter.energyMeterTask,args=())
    starkTXCallback=threading.Thread(target=flashCharger.starkTXCallback,args=())


def createEventGroups():
    print("createEventGroups is created ")
def createTimers():
    print("createTimers is created")
def vTaskStartScheduler():
    print("vTaskStartScheduler is created")

def stask():
    can1Rx.start()
    can2Rx.start()

    print("HEllo world ")
    
    chargingStationSanityTask.start()
    chargerLoop.start()
    telemetryParser.start()
    # type1Task.start()
    # idleTask.start()
    # ledTask.start()
    energyMeterTask.start()
    starkTXCallback.start()

    



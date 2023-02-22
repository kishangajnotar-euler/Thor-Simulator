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
idletask = None
energyMeterTask = None
starkTXCallback = None
initial_sanityevent = None
runtime_sanityevent = None


def createTasks():
    global can1Rx, can2Rx, idletask, starkTXCallback, chargerLoop, initial_sanityevent, runtime_sanityevent
    can1Rx = threading.Thread(target =can1)
    can2Rx = threading.Thread(target =can2)
    idletask=threading.Thread(target=chargingStationMain.idleTask)
    starkTXCallback=threading.Thread(target=flashCharger.starkTXCallback)
    chargerLoop = threading.Thread(target=chargingStationMain.chargerLoop)
    initial_sanityevent = threading.Event()
    runtime_sanityevent = threading.Event()


def stask():
    can1Rx.start()
    can2Rx.start()
    idletask.start()
    starkTXCallback.start()
    chargerLoop.start()

    



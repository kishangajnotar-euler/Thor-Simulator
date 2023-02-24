import threading
import flashCharger
from canRx1 import can1
from canRx2 import can2
from chargingStationMain import idleTask, chargerLoop, type1Task, telemetryParser

can1Rx = None 
can2Rx = None
chargingStationSanityTask = None
chargerLoopTask = None
telemetryParserTask = None
type1task = None
idletask = None
energyMeterTask = None
starkTXCallback = None
initial_sanityevent = None
runtime_sanityevent = None



def createTasks():
    global can1Rx, can2Rx, idletask, starkTXCallback, chargerLoopTask, type1task,telemetryParserTask
    can1Rx = threading.Thread(target =can1)
    can2Rx = threading.Thread(target =can2)
    idletask=threading.Thread(target=idleTask)
    starkTXCallback=threading.Thread(target=flashCharger.starkTXCallback)
    chargerLoopTask = threading.Thread(target=chargerLoop)
    

    type1task=threading.Thread(target=type1Task)
    telemetryParserTask=threading.Thread(target=telemetryParser)

def createEvent():
    global  initial_sanityevent, runtime_sanityevent
    initial_sanityevent = threading.Event()
    runtime_sanityevent = threading.Event()

def stask():
    can1Rx.start()
    can2Rx.start()
    idletask.start()
    chargerLoopTask.start()    
    starkTXCallback.start()
    telemetryParserTask.start()
    type1task.start()

def createTimers():
    chargerTXTimer_ms = 1000
    chargerTxTimer = threading.Timer(chargerTXTimer_ms/1000, flashCharger.chargerTXCallback)
    chargerTxTimer.setName("chargerTxTimer")
 

    



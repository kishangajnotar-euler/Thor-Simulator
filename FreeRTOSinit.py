import threading
import chargingStationTest
import chargingStationMain
import energyMeter
import flashCharger
import telemetryDevice
from canRx1 import can1
from canRx2 import can2
can1Rx = None 
can2Rx = None
t1

def createTasks():
    global can1Rx, can2Rx
    can1Rx = threading.Thread(target =can1)
    can2Rx = threading.Thread(target =can2)
    t1=threading.Thread(target=chargingStationTest.chargingStationSanityTask,args=())
    t2=threading.Thread(target=chargingStationMain.chargerLoop,args=())
    t3=threading.Thread(target=telemetryDevice.telemetryParser,args=())
    # t4=threading.Thread(target=type1Task,args=())
    # t5=threading.Thread(target=idleTask,args=())
    # t6=threading.Thread(target=ledTask,args=())
    t7=threading.Thread(target=energyMeter.energyMeterTask,args=())
    t8=threading.Thread(target=flashCharger.starkTXCallback,args=())


def createEventGroups():
    print("createEventGroups is created ")
def createTimers():
    print("createTimers is created")
def vTaskStartScheduler():
    print("vTaskStartScheduler is created")

def stask():
    can1Rx.start()
    can2Rx.start()
    t1.start()
    t2.start()
    t3.start()
    # t4.start()
    # t5.start()
    # t6.start()
    t7.start()
    t8.start()

    



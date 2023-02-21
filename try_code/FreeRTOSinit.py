import multiprocessing
import chargingStationTest
import chargingStationMain
import energyMeter
import flashCharger
import telemetryDevice

def createTasks():
    t1=multiprocessing.Process(target=chargingStationTest.chargingStationSanityTask,args=())
    t2=multiprocessing.Process(target=chargingStationMain.chargerLoop,args=())
    t3=multiprocessing.Process(target=telemetryDevice.telemetryParser,args=())
    # t4=multiprocessing.Process(target=type1Task,args=())
    # t5=multiprocessing.Process(target=idleTask,args=())
    # t6=multiprocessing.Process(target=ledTask,args=())
    t7=multiprocessing.Process(target=energyMeter.energyMeterTask,args=())
    t8=multiprocessing.Process(target=flashCharger.starkTXCallback,args=())
    t1.start()
    t2.start()
    t3.start()
    # t4.start()
    # t5.start()
    # t6.start()
    t7.start()
    t8.start()

def createEventGroups():
    print("createEventGroups is created ")
def createTimers():
    print("createTimers is created")
def vTaskStartScheduler():
    print("vTaskStartScheduler is created")
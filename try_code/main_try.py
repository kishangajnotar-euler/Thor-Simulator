import FreeRTOSinit

if __name__ == '__main__':
    FreeRTOSinit.createEventGroups()
    FreeRTOSinit.createTasks()
    FreeRTOSinit.createTimers()
    FreeRTOSinit.vTaskStartScheduler()
    
from tmp_declaration import syncDateTime
import time
def telemetryParser():
    while(1):
        time.sleep(3)
        xServerString="1,2,3,4,5,6,7,8,9"
        if xServerString[2] ==  8:
            syncDateTime()
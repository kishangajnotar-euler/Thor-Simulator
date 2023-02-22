from structure import *

def syncDateTime():
    # sTime = RTC_TimeTypeDef()
    # DateToUpdate = RTC_TimeTypeDef()
    buffer = [0] * 8
    buffer[0] = 15
    buffer[1] = 7
    buffer[2] = 30
    buffer[5] = 22
    buffer[6] = 2
    buffer[7] = 2023
    #Transmit_on_CAN2(rx_calander_param, S, buffer, 8)




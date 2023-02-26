import can
import logging
logging.basicConfig(filename='vec.log', filemode='a', format='%(asctime)s - %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
class Cbus: 
    def __init__(self) -> None:
        self.bus = can.interface.Bus(bustype='pcan', channel='PCAN_USBBUS1', bitrate=250000)
        # self.bus = can.interface.Bus()

    def read_data(self): 
        while True: 
            msg = self.bus.recv(timeout=2)
            if msg:

                if msg.arbitration_id == 0x402:
                    logging.info(str(msg))
            else: 
                logging.info("NULL DATA")
            
if __name__ == "__main__":
    bus = Cbus()
    bus.read_data()
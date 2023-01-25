import queue, struct, threading
from time import sleep
from serial import *
from serial.tools import list_ports

# using can-passthrough!
class ArduinoComm:
    HEADER = 0xA0.to_bytes(length=1, byteorder='big', signed=False)
    FOOTER = 0x0B.to_bytes(length=1, byteorder='big', signed=False)
    def __init__(self):
        # on_receive are functions that are called when new data is available
        self.weight = 0
        # self.temp = 0
        self.tds = 0
        self.pH = 0

        self.device_found = False
        self.serial_comm = None
        self.serial_port = None

        self.read_thread = None
        self.write_thread = None

        self.read_queue = queue.Queue()
        self.write_queue = queue.Queue()
        
        while not self.device_found:
            # get the port with the given device
            ports = list_ports.comports()
            for port in ports:
                # print(port.product)
                # print(port.)
                if port.pid == 67:  # probably better way than this, but whatever
                    self.serial_port = port.device
                    self.device_found = True
                    break
            # device not found, continue until found
            sleep(0.1)
        print(f"found serial device at {self.serial_port}")
        self.serial_comm = Serial(port=f"{self.serial_port}", baudrate=9600)
        self.read_thread = threading.Thread(target=self.read_loop, daemon=True)
        self.write_thread = threading.Thread(target=self.write_loop, daemon=True)
        self.read_thread.start()
        self.write_thread.start()

    def read_loop(self):
        # while True:
        #     if self.serial_comm.in_waiting > 0:
        #         print(self.serial_comm.read(), sep="")
        # print('a')
        while True:
            buffer = bytearray()
            data = 0
            target_len = 0
            curr_index = 0
            command = 0x00
            header_found = False
            while True:
                if self.serial_comm.in_waiting > 0:
                    val = self.serial_comm.read()
                    if not header_found:
                        if val == ArduinoComm.HEADER:
                            header_found = True
                            curr_index += 1
                    elif curr_index == 1:
                        command = int.from_bytes(val, "big")
                        match command:
                            case _:
                                target_len = 4
                        curr_index += 1
                    elif curr_index-2 < target_len:
                        buffer += val
                        curr_index += 1
                    else:
                        if val == ArduinoComm.FOOTER:
                            data = (struct.unpack("=f", buffer))[0]
                            match (command):
                                case 0x01:  #weight
                                    self.weight = data
                                    print("weight: " + str(self.weight))
                                case 0x02:  #pH
                                    self.pH = data
                                    print("pH: " + str(self.pH))
                                case 0x03:  #tds
                                    self.tds = data
                                    print("tds: " + str(self.tds))
                        break
       

    def write_loop(self):
        while True:
            if self.write_queue.not_empty:
                self.serial_comm.write(self.write_queue.get())

    def feed_once(self):
        self.feed_num()

    def feed_num(self, num_time=1):
        if type(num_time) == int:
            self.write_queue.put(struct.pack("=ccic"),ArduinoComm.HEADER, 0x1A.to_bytes(length=1, byteorder='big', signed=False), num_time, ArduinoComm.FOOTER)

if __name__ == "__main__":
    comms = ArduinoComm()
    while True:
        sleep(0.1)
        # print("weight: " + str(comms.weight))
        # print("pH:" + str(comms.pH))
        # print("temp: " + str(comms.temp))
        # print("tds: " + str(comms.tds))
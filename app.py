import serial
import serial.tools.list_ports
import struct
import json
import time
import threading

class Arduino(serial.Serial):
    def __init__(self):
        super().__init__()
        try:
            for port in serial.tools.list_ports.comports():
                if port.pid == 0x7523 and port.vid == 0x1a86:
                    self.port = port.device
            self.baudrate = 115200
            self.timeout = 0.1
            self.open()
        except Exception as e:
            print(e)

class App():
    def __init__(self):
        self.arduino = Arduino()

        t_0 = threading.Thread(target=self.handle_serial)
        t_0.daemon = True
        t_0.start()

    def handle_serial(self):
        buffer = bytearray()
        while True:
            try:
                buffer = self.arduino.readline()
            except Exception as e:
                print(e)
                # break
            if buffer:
                print(f'device returns: {buffer}')
                line = buffer.decode('utf-8')
                line_stripped = line.rstrip()
                j = json.loads(line_stripped)
                print(j['value'], j['date'], j['time'])
                # break

    def get_status(self, id):
        while True:
            self.arduino.write(b'get status\r')
            buffer = self.arduino.readline()
            if buffer:
                if buffer == b'OK\n':
                    break
            time.sleep(1)

    def get_voltage(self, id):
        # self.arduino.write(b'get voltage\r')
        # # self.arduino.write(struct.pack('<h', 1))
        # buffer = b''
        # while True:
        #     if b'\n' in buffer:
                
        #     else:
        #         buffer += self.arduino.read(1)
        #     buffer += self.arduino.read(self.arduino.in_waiting)
        #     print(len(buffer))
        #     # if len(buffer) == 4:
        #     #     break
        # print(buffer)
        # print(struct.unpack('hh', self.arduino.read(4)))
        pass

    def get_resistance(self, id):
        pass

def main():
    app = App()
    while True:
        pass

if __name__ == "__main__":
    main()
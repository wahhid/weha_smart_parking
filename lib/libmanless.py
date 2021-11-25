import threading
import serial
import time 

class ManlessDevice(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        self._running = True
        self.connected = False
        self.connect()

    def connect(self):
        if not self.connected:
            self.ser = serial.Serial('/dev/cu.usbmodem14201', 9600, timeout=1)
            self.connected = True

    def terminate(self):
        self._running = False

    def run(self):
            data = ''
            greeting = True
            self.connected = False
            while not self.connected:
                #serin = ser.read()
                self.connect()
                while self._running and True:
                    try:
                        if not self.connected:
                            self.connect()
                        receive = self.ser.read()
                        data = data + receive.decode('utf-8')
                        if len(data) == 4:
                            print(data)
                            if data == "1000":
                                print("CAR DETECTED")
                                #CAR_DETECTED = True
                                if greeting:
                                    print("Run Greeting")
                                    greeting = False
                                    #x = threading.Thread(target=thread_function, args=(1,))
                                    #x.start()
                            if data == "2000":
                                print("ENTRY BUTTON PRESSED")
                                time.sleep(5)
                                self.create_transaction()
                                greeting = True
                            if data == "8001":
                                print("CAR NOT DETECTED")
                                #CAR_DETECTED = False
                            if data == "8002":
                                print('RESET DEVICE')
                                greeting = True
                            data = ""
                    except Exception as ex:
                        print(ex)
                        print("No Serial Device")
                        self.connected = False                    

    def create_transaction(self):
        print("Create Transaction")
        self.ser.write("8000".encode())

    def test_print(self):
        print("Test Print")

#device = ManlessDevice()
#device.start()
#device.test_print()
#thread = threading.Thread(target=read_from_port, args=(serial_port,))
#thread.start()
# thread.onThread(thread.handle_data("test"))

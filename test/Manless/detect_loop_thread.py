import threading
import serial

connected = False
port = '/dev/cu.usbmodem14201'
baud = 9600

serial_port = serial.Serial(port, baud, timeout=0)

def handle_data(data):
    print(data)

def read_from_port(ser):
    data = ''
    connected = False
    while not connected:
        #serin = ser.read()
        connected = True
        while True:
            receive = ser.read()
            data = data + receive.decode('utf-8')
            if len(data) == 4:
                print(data)
                data = ''

thread = threading.Thread(target=read_from_port, args=(serial_port,))
thread.start()
# thread.onThread(thread.handle_data("test"))

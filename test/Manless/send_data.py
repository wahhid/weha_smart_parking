import serial

ser = serial.Serial('/dev/cu.usbmodem14201', 9600, timeout=1)

ser.write("8000".encode())

data = ''
while True:
    receive = ser.read()
    data = data + receive.decode('utf-8')
    if len(data) == 4:
        print(data)
        break
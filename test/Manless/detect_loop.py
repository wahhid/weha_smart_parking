import pyfirmata
import time

board = pyfirmata.Arduino('/dev/cu.usbmodem14201')
relay1=board.get_pin('d:13:o')

while True:
    relay1.write(1)
    time.sleep(1)
    relay1.write(0)
    time.sleep(1)
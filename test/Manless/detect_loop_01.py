
import serial
import time
import threading 
import gtts
from playsound import playsound

greeting = True

def clearGreeting():
    print("Clearing")
    greeting = True

def thread_function(name):
    tts = gtts.gTTS("Selamat Datang di Mal Taman Anggrek, Tekan Tombol atau Tap Kartu Langganan Anda", lang="id")
    tts.save("hola.mp3")
    playsound("hola.mp3")
    #time.sleep(10000)
    clearGreeting()

def create_transaction():
    print("Create Transaction")
    ser.write("8000".encode())

ser = serial.Serial('/dev/cu.usbmodem14201', 9600, timeout=1)
data = ""
CAR_DETECTED = False

while True:
    receive = ser.read()
    data = data + receive.decode('utf-8')
    if len(data) == 4:
        print(data)
        if data == "1000":
            print("CAR DETECTED")
            CAR_DETECTED = True
            if greeting:
                print("Run Greeting")
                greeting = False
                x = threading.Thread(target=thread_function, args=(1,))
                x.start()
        if data == "2000":
            print("ENTRY BUTTON PRESSED")
            time.sleep(5)
            create_transaction()
            greeting = True
        if data == "8001":
            print("CAR NOT DETECTED")
            CAR_DETECTED = False
        if data == "8002":
            print('RESET DEVICE')
            greeting = True
        data = ""
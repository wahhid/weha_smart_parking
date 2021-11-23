import serial

def calculate_checksum(data_before):
    #print(data_before)
    last_data = ""
    for i in range(0, len(data_before), 2):
        #print(data_before[i:i+2])   
        if i > 0:
            current_xor = hex(int(last_data,16) ^ int( "0x" + data_before[i:i+2], 16))
            last_data = current_xor
            #print(current_xor)
        else:
            last_data = "0x" + data_before[i:i+2]
    return current_xor
    #for elem in data_before[ : : 2]: 
    #    print(elem)


ser = serial.Serial('/dev/tty.UC-232AC',  38400, timeout=13)
print(ser.name)
#input = [0x41]
#ser.write(serial.to_bytes(input))
#ser.write(input.encode('utf-8')) 

STARTCODE="1002"
HEADER="08000100000000"
LENGTH="0001"
USERDATA="42"
CHECKSUM="4A"
ENDCODE="1003"
data_before = HEADER + LENGTH + USERDATA
#CHECKSUM = calculate_checksum(data_before)
print(CHECKSUM)

SIGNON = STARTCODE + HEADER + "0001" + "42" + "4A" + ENDCODE
print(SIGNON)
message_bytes = bytes.fromhex(SIGNON)

result = ser.write(message_bytes)
print("Write total bytes:",result)\

print("STARTCODE")
#STARTCODE
#LENGTH 2
count=0
HEXDATA = ""
while count < 2:
    for line in ser.read(1):
        #print(count)
        count = count + 1
        #print(line)
        #print(hex(line)[2:4].zfill(2))
        HEXDATA = HEXDATA + hex(line)[2:4].zfill(2)
    #print("Finished")
print(HEXDATA)

print("HEADER")
#HEADER
#LENGTH 7
count=0
HEXDATA = ""
while count < 7:
    for line in ser.read(1):
        #print(count)
        count = count + 1
        #print(line)
        #print(hex(line)[2:4].zfill(2))
        HEXDATA = HEXDATA + hex(line)[2:4].zfill(2)
    #print("Finished")
print(HEXDATA)


print("LENGTH")
#LENGTH
#LENGTH 3
count=0
HEXDATA = ""
while count < 3:
    for line in ser.read(1):
        #print(count)
        count = count + 1
        #print(line)
        #print(hex(line)[2:4].zfill(2))
        HEXDATA = HEXDATA + hex(line)[2:4].zfill(2)
    #print("Finished")
print(HEXDATA)
#data_length = int(HEXDATA,16)
#print(data_length)

print("DATA")
#LENGTH
#LENGTH 16
count=0
HEXDATA = ""
while count < 16:
    for line in ser.read(1):
        #print(count)
        count = count + 1
        #print(line)
        #print(hex(line)[2:4].zfill(2))
        HEXDATA = HEXDATA + hex(line)[2:4].zfill(2)
    #print("Finished")
print(HEXDATA)

ser.close()


#100208000200000000001F423030303030303030353138393634303134353030373930303030303230305C1003
#1028020000010104130303030515033303030495056323216103
#DOCUMENT
#10020800020000000000101041303030305150333030304950563231151003
#PROGRAM
#10020800020000000000101041303030305150333030304950563232161003
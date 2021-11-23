import serial

def encode_data(STARTCODE, HEADER, AMOUNT, TANGGAL, KODEPERINTAH):
    STARTCODE="1002"
    HEADER="08000100000000"
    AMOUNT="30303030303030303031"
    TANGGAL="3230313430343134313330363132"
    USERDATA = KODEPERINTAH + AMOUNT + TANGGAL
    data_length = len(USERDATA) / 2
    #print(data_length)
    a = hex(int(data_length))
    #print(a[2:len(a)].zfill(4))

    #LENGTH="0019"
    LENGTH=a[2:len(a)].zfill(4)
    #CHECKSUM 49
    ENDCODE="1003"
    data_before = HEADER + LENGTH + USERDATA
    CHECKSUM = calculate_checksum(data_before)
    print(CHECKSUM)

    PAYMENT = STARTCODE + HEADER + LENGTH + USERDATA + CHECKSUM[2:4] + ENDCODE
    print(PAYMENT)
    return PAYMENT

def parsing_payment_data(PAYMENTDATA_ASCII):
    vals = {
        'data01': PAYMENTDATA_ASCII[0:16],
        'data02': PAYMENTDATA_ASCII[16:22],
        'data03': PAYMENTDATA_ASCII[22:36],
        'data04': PAYMENTDATA_ASCII[36:46],
        'data05': PAYMENTDATA_ASCII[46:56],
        'data06': PAYMENTDATA_ASCII[56:57],
        'data07': PAYMENTDATA_ASCII[57:65],
        'data08': PAYMENTDATA_ASCII[65:73],
        'data09': PAYMENTDATA_ASCII[73:89],
        'data10': PAYMENTDATA_ASCII[89:105],
        'data11': PAYMENTDATA_ASCII[105:113],
        'data12': PAYMENTDATA_ASCII[113:119],
        'data13': PAYMENTDATA_ASCII[119:123],
        'data14': PAYMENTDATA_ASCII[123:135],
        'data15': PAYMENTDATA_ASCII[135:143],
        'data16': PAYMENTDATA_ASCII[143:159],
        'data17': PAYMENTDATA_ASCII[159:161],
        'data18': PAYMENTDATA_ASCII[161:165],
        'data19': PAYMENTDATA_ASCII[165:185],
        
    }
    return vals

def generate_txn_row(vals):
    pass    

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
    #print(current_xor)
    return current_xor


#CONNET TO DEVICE
ser = serial.Serial('/dev/tty.UC-232AC',  38400, timeout=8)
print(ser.name)



#TEST_PAYMENT = "100208000100000000001943303030303030303030313230313430343134313330363132531003"
#print(TEST_PAYMENT)

STARTCODE="1002"
HEADER="08000100000000"
AMOUNT="30303030303030303031"
TANGGAL="3230313430343134313330363132"
KODEPERINTAH="43"
PAYMENT = encode_data(STARTCODE,HEADER,AMOUNT,TANGGAL, KODEPERINTAH)
message_bytes = bytes.fromhex(PAYMENT)

result = ser.write(message_bytes)
print("Write total bytes:",result)
count=0
#length 19
arr_int = []
arr_ascii = []
PAYMENTINITRESPONSE = ''
while count < 19:
    for line in ser.read(1):
        #print(count)
        count = count + 1
        #print(line)
        #print(hex(line)[2:4].zfill(2))
        arr_int.append(line)
        arr_ascii.append(chr(line))
        PAYMENTINITRESPONSE = PAYMENTINITRESPONSE + hex(line)[2:4].zfill(2)
    #print("Finished")
print(PAYMENTINITRESPONSE)
print(arr_int)
print(arr_ascii)

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
data_length = int(HEXDATA,16)
#print(data_length)

#DATA
#LENGTH data_length
count=0
HEXDATA = ""
while count < data_length:
    for line in ser.read(1):
        #print(count)
        count = count + 1
        #print(line)
        #print(hex(line)[2:4].zfill(2))
        HEXDATA = HEXDATA + hex(line)[2:4].zfill(2) 
    #print("Finished")
print(HEXDATA)
USERDATA = HEXDATA
KODEPERINTAH = USERDATA[0:2]
print(KODEPERINTAH)
RESPONSECODE = USERDATA[2:10]
print(RESPONSECODE)
PAYMENTDATA = USERDATA[10:len(USERDATA)]
print(PAYMENTDATA)
PAYMENTDATA_ASCII = bytes.fromhex(PAYMENTDATA).decode('utf-8')
print(PAYMENTDATA_ASCII)
vals_payment = parsing_payment_data(PAYMENTDATA_ASCII)
print("FLAZZ Card PAN                           : " + vals_payment['data01'])
print("FLAZZ Card expired date                  : " + vals_payment['data02'])
print("Trans. Date & Time                       : " + vals_payment['data03'])
print("FLAZZ Card Balance                       : " + vals_payment['data04'])
print("Payment Amount                           : " + vals_payment['data05'])
print("Completion code                          : " + vals_payment['data06'])
print("P-SAM Identity                           : " + vals_payment['data07'])
print("P-SAM Trans. No. (TTC)                   : " + vals_payment['data08'])
print("P-SAM Random No (Rterm)                  : " + vals_payment['data09'])
print("P-SAM Cryptogram (Cterm)                 : " + vals_payment['data10'])
print("FLAZZ card Cryptogram (Ccard3..0)        : " + vals_payment['data11'])
print("FLAZZ card Trans. No (CTC)               : " + vals_payment['data12'])
print("FLAZZ card Debit Certificate (CDC7..6)   : " + vals_payment['data13'])
print("Merchant ID                              : " + vals_payment['data14'])
print("Terminal ID                              : " + vals_payment['data15'])
print("TRN                                      : " + vals_payment['data16'])
print("FLAZZ Data Version                       : " + vals_payment['data17'])
print("FLAZZ Card track-2 expired date          : " + vals_payment['data18'])
print("Reserved                                 : " + vals_payment['data19'])


print("CHECKSUM")
#LENGTH
#LENGTH 1
count=0
HEXDATA = ""
while count < 1:
    for line in ser.read(1):
        #print(count)
        count = count + 1
        #print(line)
        #print(hex(line)[2:4].zfill(2))
        HEXDATA = HEXDATA + hex(line)[2:4].zfill(2)
    #print("Finished")
print(HEXDATA)

print("ENDCODE")
#LENGTH
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
ser.close()


#SAMA
#DOCUMENT
#43303030303031343530303238303030303031333730313033323432303134303431343133303631323030303035333339393530303030303030303031303030303030303033303030303033324436423437303944394431304346414341314131353230373334324633364543343939424341414139303030303246454234453838353030303031353939394543523030303031464530303731374646443434423131343031343931323030303030303030303030303030303030303030
#PROGRAM
#43303030303031343530303732303332363830313732393038323632303134303431343133303631323030303030343939373630303030303030303031303030313033353730303030303033313537463830343544363031433438394545304135373236334335364538303737373937364446463238303030303238303135303838353030303835393131344543524d4d544133323439334146334630353236414646453031343931323030303030303030303030303030303030303030

#SAMA
#DOCUMENT PAYMENT DATA
#014500280000013701032420140414130612000053399400000000010000000030000032EF7CC6D1BC91570A040AAACD5A48F908E8CB81E460000315B24885000015999ECR00001A39C307F536ADBA401491200000000000000000000
#PROGRAM PAYMENT DATA
#014500280000013701032420140414130612000053399400000000010000000030000032EF7CC6D1BC91570A040AAACD5A48F908E8CB81E460000315B24885000015999ECR00001A39C307F536ADBA401491200000000000000000000

#PAYMENT DATA
#FLAZZ Card PAN                           : 0145007203268017
#FLAZZ Card expired date                  : 290826
#Trans. Date & Time                       : 20140414130612
#FLAZZ Card Balance                       : 0000049957
#Payment Amount                           : 0000000001
#Completion code                          : 0
#P-SAM Identity                           : 00103570
#P-SAM Trans. No. (TTC)                   : 00000328
#P-SAM Random No (Rterm)                  : E51B2F2842F8DE84
#P-SAM Cryptogram (Cterm)                 : F8BCD028AE02E082
#FLAZZ card Cryptogram (Ccard3..0)        : 96F0D9F1
#FLAZZ card Trans. No (CTC)               : 00003B
#FLAZZ card Debit Certificate (CDC7..6)   : 21C2
#Merchant ID                              : 885000859114
#Terminal ID                              : ECRMMTA3
#TRN                                      : 9BA2F91889BA3DDE
#FLAZZ Data Version                       : 01
#FLAZZ Card track-2 expired date          : 4912
#Reserved                                 : 00000000000000000000


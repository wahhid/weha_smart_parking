import serial
from . errorhandling import ErrorHandling
from . utils import Utils

class BcaFlazzLibrary:

    def __init__(self, port, baudrate, timeout=13):
        super(BcaFlazzLibrary, self).__init__()
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.connected = False
        self.utils = Utils()

    def connect(self):
        try:
            self.ser = serial.Serial(self.port,  self.baudrate, timeout=self.timeout)
            print (self.ser.write_timeout)
            self.connected = True
            return ErrorHandling(False, "Connect serial successfully")
        except serial.SerialException as e:
            return ErrorHandling(True, "Connect serial problem")
    
    def signon(self):
        if not self.connected:
            return ErrorHandling(True, "Flazz Reader not ready, please connect reader first")
        else:
            try:
                STARTCODE="1002"
                HEADER="08000100000000"
                USERDATA="41"

                LENGTH="0001"
                #CHECKSUM 49
                ENDCODE="1003"
                data_before = HEADER + "0001" + USERDATA
                CHECKSUM = self.utils.calculate_checksum(data_before)
                print(CHECKSUM)

                SIGNON = STARTCODE + HEADER + "0001" + "41" + "49" + ENDCODE
                print(SIGNON)
                message_bytes = bytes.fromhex(SIGNON)

                result = self.ser.write(message_bytes)
                print("Write total bytes:",result)

                print("STARTCODE")
                #STARTCODE
                #LENGTH 2
                count=0
                HEXDATA = ""
                while count < 2:
                    for line in self.ser.read(1):
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
                    for line in self.ser.read(1):
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
                    for line in self.ser.read(1):
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
                    for line in self.ser.read(1):
                        #print(count)
                        count = count + 1
                        #print(line)
                        #print(hex(line)[2:4].zfill(2))
                        HEXDATA = HEXDATA + hex(line)[2:4].zfill(2)
                    #print("Finished")
                return ErrorHandling(False, 'Sign On')
            except serial.SerialException as e:
                return ErrorHandling(True, 'Error Serial Timeout')

    def payment(self):
        if not self.connected:
            return ErrorHandling(True, "Flazz Reader not ready, please connect reader first")
        else:
            STARTCODE="1002"
            HEADER="08000100000000"
            AMOUNT="30303030303030303031"
            TANGGAL="3230313430343134313330363132"
            KODEPERINTAH="43"
            PAYMENT = self._encode_data(STARTCODE,HEADER,AMOUNT,TANGGAL, KODEPERINTAH)
            message_bytes = bytes.fromhex(PAYMENT)

            result = self.ser.write(message_bytes)
            print("Write total bytes:",result)
            count=0
            #length 19
            arr_int = []
            arr_ascii = []
            PAYMENTINITRESPONSE = ''
            while count < 19:
                for line in self.ser.read(1):
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
                for line in self.ser.read(1):
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
                for line in self.ser.read(1):
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
                for line in self.ser.read(1):
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
                for line in self.ser.read(1):
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
            vals_payment = self._parsing_payment_data(PAYMENTDATA_ASCII)
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
                for line in self.ser.read(1):
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
                for line in self.ser.read(1):
                    #print(count)
                    count = count + 1
                    #print(line)
                    #print(hex(line)[2:4].zfill(2))
                    HEXDATA = HEXDATA + hex(line)[2:4].zfill(2)
                #print("Finished")
            print(HEXDATA)
            return ErrorHandling(False, "Payment Successfully")

    def _encode_data(self, STARTCODE, HEADER, AMOUNT, TANGGAL, KODEPERINTAH):
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
        CHECKSUM = self.utils.calculate_checksum(data_before)
        print(CHECKSUM)

        PAYMENT = STARTCODE + HEADER + LENGTH + USERDATA + CHECKSUM[2:4] + ENDCODE
        print(PAYMENT)
        return PAYMENT

    def _parsing_payment_data(self, PAYMENTDATA_ASCII):
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

    def _generate_txn_row(vals):
        pass    


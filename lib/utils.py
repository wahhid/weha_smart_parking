
class Utils:
    
    def __init__(self):
        super(Utils, self).__init__()

    def calculate_checksum(self, data_before):
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
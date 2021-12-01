
'''

parameters.py
This module holds all fucntions and logic related to parameters. 

'''

def writeParam(inList):
    # Writes parameters to local storage file. 


    file1 = open("parameters.txt", "w")

    for line in inList:
        file1.write(str(line) + "\n")

    file1.close()



def readParam():
    # Reads parameters from local storage file. 

    outList = []

    file1 = open("parameters.txt", "r")
    for line in file1.readlines():
        outList.append(line.strip("\n"))
    file1.close

    return outList



def validate(inputList):
    # Takes in all the inputted parameters (which are strings) and returns 1 iff all paramaters are valid.

    for i in range(0, inputList.length):
        if (inputList[i] != ""):

            # Parameter 0 : Lower Rate Limit 
            if (i == 0):
                num = int(inputList[i])
                if (30 <= num <= 50) or (90 <= num <= 175):
                    if (num % 5 != 0):
                        return 0
                if (num > 175 or num < 30):
                    return 0
            
            # Parameter 1 : Upper Rate Limit 
            if (i == 1):
                num = int(inputList[i])
                if (num > 175 or num < 50):
                    return 0
                elif (num % 5 != 0):
                    return 0

            # Parameter 2 : Maximum Sensor Rate 
            if (i == 2):
                num = int(inputList[i])
                if (num > 175 or num < 50):
                    return 0
                elif (num % 5 != 0):
                    return 0

            # Parameter 3 : Fixed AV Delay
            if (i == 3):
                num = int(inputList[i])

    return 1



# Sending parameters to pacemaker using serial communication. 

# Import Libraries
import serial 
import struct

# Establish Serial Connection 
ser = serial.Serial()
ser.port = "COM4"
ser.baudrate = 115200

# Define Fucntion
def sendParam(parmsList):

    # Collecting Data
    packet = [] # Holds all data for each transmission
    packet.append(b'\x16') # Init
    packet.append(b'\x55') # set-param code
    packet.append(struct.pack('<H', 10))
    packet.append(struct.pack('<H', 60))
    packet.append(struct.pack('<H', 120))
    packet.append(struct.pack('<H', 250))
    packet.append(struct.pack('<H', 150))
    packet.append(struct.pack('<H', 10))
    packet.append(struct.pack('<H', 16))
    packet.append(struct.pack('<d', 0.2))#act-thresh
    packet.append(struct.pack('<H', 20))
    packet.append(struct.pack('<H', 180))
    packet.append(struct.pack('<d', 3.5))
    packet.append(struct.pack('<H', 10))
    packet.append(struct.pack('<H', 200))#ARP
    packet.append(struct.pack('<d', 1.8))
    packet.append(struct.pack('<d', 2.4))
    packet.append(struct.pack('<d', 3.5))
    packet.append(struct.pack('<H', 10))
    packet.append(struct.pack('<H', 200))
    packet.append(struct.pack('<d', 2.2))
    packet.append(struct.pack('<d', 2.4)) 
    
    # Sending Data
    ser.open()
    for pack in packet:
        ser.write(pack)
    ser.close()




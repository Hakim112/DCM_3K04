
'''

parameters.py
This module holds all fucntions and logic related to parameters. 

'''

from os import read


def writeParam(inList):
    # Writes parameters to local storage file. 

    currentParams = readParam()

    file1 = open("parameters.txt", "w")

    for i in range(len(inList)):
        if (inList[i] == ""):
            file1.write(str(currentParams[i]) + "\n")
        else:
            file1.write(str(inList[i]) + "\n")

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
    # Takes in all the inputted parameters (which are strings) and returns a string of 1s iff all paramaters are valid.

    valids = ""

    # Parameter 0 : Mode 
    valids += "1"

    for i in range(len(inputList)):
        value = inputList[i]

        # Any blank value means no change, therefore input is valid
        if  value == "":
            valids += "1"

        # All non-blank values need to be validated based on parameter
        else:

            # Parameter 1 : Lower Rate Limit 
            if i == 1:
                val = int(value) # ASSUMING VALUES ARE ALL INTS
                if (30 <= val <= 50) & (val % 5 == 0):
                    valids += "1"
                elif (50 <= val <= 90):
                    valids += "1"
                elif (90 <= val <= 175) & (val % 5 == 0):
                    valids += "1"
                else:
                    valids += "0"
                
            # Parameter 2 : Upper Rate Limit 
            elif i == 2:
                val = int(value)
                if (50 <= val <= 175) & (val % 5 == 0):
                    valids += "1"
                else:
                    valids += "0"
            
            # Parameter 3 : Fixed AV Delay
            elif i == 3:
                val = int(value)
                if (70 <= val <= 300) & (val % 10 == 0):
                    valids += "1"
                else:
                    valids += "0"

            # Parameter 4 : Reaction Time
            elif i == 4:
                val = int(value)
                if (10 <= val <= 50) & (val % 10 == 0):
                    valids += "1"
                else:
                    valids += "0"
            
            # Parameter 5 : Response Factor
            elif i == 5:
                val = int(value)
                if (1 <= val <= 16):
                    valids += "1"
                else:
                    valids += "0"

            # Parameter 6 : Activity Threshold
            elif i == 6:
                valids += "1"

            # Parameter 7 : Recovery Time
            elif i == 7:
                val = int(value)
                if (2 <= val <= 16):
                    valids += "1"
                else:
                    valids += "0"

            # Parameter 8 : Maximum Sensor Rate
            elif i == 8:
                val = int(value)
                if (50 <= val <= 175) & (val % 5 == 0):
                    valids += "1"
                else:
                    valids += "0"



            # Parameter 9 : Atrial Amplitude     ASSUMING UNREG
            elif i == 9:
                valids += "1"

            # Parameter 10 : Atrial Pulse Width 
            elif i == 10:
                val = int(value)
                if (1 <= val <= 30) & (val % 1 == 0):
                    valids += "1"
                else:
                    valids += "0"

                # val = float(value)
                # if (val == 0.05):
                #     valids += "1"
                # elif (0.1 <= val <= 1.9) & (val % 0.1 == 0):
                #     valids += "1"
                # else:
                #     valids += "0"
            
            # Parameter 11 : ARP 
            elif i == 11:
                val = int(value)
                if (150 <= val <= 500) & (val % 10 == 0):
                    valids += "1"
                else:
                    valids += "0"

                # val = float(value)
                # if (val == 0):
                #     valids += "1"
                # elif (0.5 <= val <= 3.2) & (val % 0.1 == 0):
                #     valids += "1"
                # elif (3.5 <= val <= 7.0) & (val % 0.5 == 0):
                #     valids += "1"
                # else:
                #     valids += "0"

            # Parameter 12 : Atrial Threshold   IS THIS NEEDED??
            elif i == 12:
                valids += "1"

            # Parameter 13 : Atrial Sensitivity 
            elif i == 13:
                val = float(value)
                if (0 <= val <= 5) & (val % 0.1 == 0):
                    valids += "1"
                else:
                    valids += "0"

            # Parameter 14 : Ventricular Amplitude 
            elif i == 14:     # NEED CLEARIFICATION: REG OR UNREG?
                valids += "1"
            
            # Parameter 15 : Ventricular Pulse Width
            elif i == 15:
                val = int(value)
                if (1 <= val <= 30) & (val % 1 == 0):
                    valids += "1"
                else:
                    valids += "0"
            
            # Parameter 16 : VRP
            elif i == 16:
                val = int(value)
                if (150 <= val <= 500) & (val % 10 == 0):
                    valids += "1"
                else:
                    valids += "0"
            
            # Parameter 17 : Ventricular Threshold  IS THIS NEEDED??
            elif i == 17: 
                valids += "1"
            
            # Parameter 18 : Ventricular Sensitivity 
            elif i == 18:
                val = float(value)
                if (0 <= val <= 5) & (val % 0.1 == 0):
                    valids += "1"
                else:
                    valids += "0"

    return valids




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


def validateSend(sentList):

    # WHY ARE TOLERENCES IN MS??
    
    receivedList = receiveParam()

    if(len(sentList) != len(receivedList)):
        return 0

    for i in range(len(sentList)):
        if (sentList[i] != receivedList[i]):
            return 0

    return 1

def receiveParam():

    # NEED SIMULINK PEOPLE TO COME THROUGH 
    # listR = readParam()
    listR = ['DDD', '61', '120', '150', '30', '8', 'Med', '5', '120', '3.75', '1', '250', '!', '2.5', '3.75', '1', '320', '!', '2.5']
    print(listR)


    return listR
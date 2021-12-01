
'''

parameters.py
This module holds all fucntions and logic related to parameters. 

'''


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

            # Parameter 9 : Atrial Amplitude   
            elif i == 9:
                valids += "1"

            # Parameter 10 : Atrial Pulse Width 
            elif i == 10:
                val = int(value)
                if (1 <= val <= 30) & (val % 1 == 0):
                    valids += "1"
                else:
                    valids += "0"
            
            # Parameter 11 : ARP 
            elif i == 11:
                val = int(value)
                if (150 <= val <= 500) & (val % 10 == 0):
                    valids += "1"
                else:
                    valids += "0"

            # Parameter 12 : Atrial Sensitivity 
            elif i == 12:
                val = float(value)
                if (0 <= val <= 5) & (val % 0.1 == 0):
                    valids += "1"
                else:
                    valids += "0"

            # Parameter 13 : Ventricular Amplitude 
            elif i == 13: 
                valids += "1"
            
            # Parameter 14 : Ventricular Pulse Width
            elif i == 14:
                val = int(value)
                if (1 <= val <= 30) & (val % 1 == 0):
                    valids += "1"
                else:
                    valids += "0"
            
            # Parameter 15 : VRP
            elif i == 15:
                val = int(value)
                if (150 <= val <= 500) & (val % 10 == 0):
                    valids += "1"
                else:
                    valids += "0"
            
            # Parameter 16 : Ventricular Sensitivity 
            elif i == 16:
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
    packet.append(struct.pack('<B', int(parmsList[0])))  # Mode
    packet.append(struct.pack('<B', int(parmsList[1])))  # LRR 
    packet.append(struct.pack('<B', int(parmsList[2])))  # URR
    packet.append(struct.pack('<H', int(parmsList[3])))  # Fixed AV Delay
    packet.append(struct.pack('<B', int(parmsList[4])))  # Reaction time
    packet.append(struct.pack('<B', int(parmsList[5])))  # Response Factor 

    # Act Thresh
    if (parmsList[6] == "V-Low"):
        packet.append(struct.pack('<d', 0.0)) 
    elif (parmsList[6] == "Low"):
        packet.append(struct.pack('<d', 0.0)) 
    elif (parmsList[6] == "Med-Low"):
        packet.append(struct.pack('<d', 0.1)) 
    elif (parmsList[6] == "Med"): # nom
        packet.append(struct.pack('<d', 0.2)) 
    elif (parmsList[6] == "Med-High"):
        packet.append(struct.pack('<d', 0.3)) 
    elif (parmsList[6] == "High"):
        packet.append(struct.pack('<d', 0.4)) 
    elif (parmsList[6] == "V-High"):
        packet.append(struct.pack('<d', 0.5)) 

    packet.append(struct.pack('<B', int(parmsList[7])))    # Recovery Time
    packet.append(struct.pack('<B', int(parmsList[8])))    # Max Sensor Rate
    packet.append(struct.pack('<d', float(parmsList[9])))  # Atrial Amp
    packet.append(struct.pack('<B', int(parmsList[10])))   # Atrial Pulse Width
    packet.append(struct.pack('<H', int(parmsList[11])))   # ARP
    packet.append(struct.pack('<d', 1.8))                  # ATRIAL THRESHOLD
    packet.append(struct.pack('<d', float(parmsList[12]))) # Atrial Sens
    packet.append(struct.pack('<d', float(parmsList[13]))) # Vent Amp
    packet.append(struct.pack('<B', int(parmsList[14])))   # Vent Pulse Width
    packet.append(struct.pack('<H', int(parmsList[15])))   # VRP
    packet.append(struct.pack('<d', 1.8))                  # VENTRICULAR THRESHOLD
    packet.append(struct.pack('<d', float(parmsList[16]))) # Vent sens
    
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
    listR = readParam()
    # listR = ['DDD', '61', '120', '150', '30', '8', 'Med', '5', '120', '3.75', '1', '250', '!', '2.5', '3.75', '1', '320', '!', '2.5']
    print(listR)


    return listR
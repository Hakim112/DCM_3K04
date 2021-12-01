
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



    # Parameter 1 : Lower Rate Limit 

    # Parameter 2 : Upper Rate Limit 

    # Parameter 3 : Fixed AV Delay

    # Parameter 4 : Reaction Time

    # Parameter 5 : Response Factor

    # Parameter 6 : Activity Threshold

    # Parameter 7 : Recovery Time

    # Parameter 8 : Maximum Sensor Rate 

    # Parameter 9 : Atrial Amplitude 

    # Parameter 10 : Atrial Pulse Width 

    # Parameter 11 : ARP 

    # Parameter 12 : Atrial Threshold 
    
    # Parameter 13 : Atrial Sensitivity 

    # Parameter 14 : Ventricular Amplitude 

    # Parameter 15 : Ventricular Pulse Width 

    # Parameter 16 : VRP 

    # Parameter 17 : Ventricular Threshold 
    
    # Parameter 18 : Ventricular Sensitivity 
    
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




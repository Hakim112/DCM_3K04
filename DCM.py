'''

DEVICE CONTROL MONITOR (DCM)
SFWRENG 3K04 

TODO
- Modularize code
- Input Validation 
- Testing

'''

# Importing Libraries 
import PySimpleGUI as sg  
import serial 
import struct

# Importing Modules 
import parameters
import users
import gui


# gui.welcome()

import os
cwd = os.getcwd()
print(cwd)
print(os.listdir(cwd))
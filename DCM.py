'''

DEVICE CONTROL MONITOR (DCM)
SFWRENG 3K04 

TODO
- Pacing Mode 
- CommIndicator
- Input Validation 
- Add new parameters 

'''

# Importing Libraries 
import PySimpleGUI as sg  
import serial 
import struct

# Importing Modules 
import gui


gui.welcome()

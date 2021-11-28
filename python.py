'''

DEVICE CONTROL MONITOR (DCM)
SFWRENG 3K04 

'''


# Importing Libraries 
import PySimpleGUI as sg  


import serial 
import struct

# HOW DOES THIS WORK WITH struct.pack ?

# Establish Serial Connection 
ser = serial.Serial()
ser.port = "COM5"
ser.baudrate = 115200


def sendParam(parmsList):
    
    packets = []
    packets.append(struct.pack('<B', 22)) # Init
    packets.append(struct.pack('<B', 85)) # set-param code
    packets.append(struct.pack('<B', 0))
    packets.append(struct.pack('<H', 0))
    packets.append(struct.pack('<H', 0))
    packets.append(struct.pack('<B', 0))
    packets.append(struct.pack('<H', 0))
    packets.append(struct.pack('<d', 0))
    packets.append(struct.pack('<d', 0))
    packets.append(struct.pack('<f', 0))
    packets.append(struct.pack('<f', 0))
    packets.append(struct.pack('<H', 0))
    packets.append(struct.pack('<H', 0))
    packets.append(struct.pack('<f', 0))
    packets.append(struct.pack('<B', 0))
    packets.append(struct.pack('<B', 0))
    
    ser.open()
    for packet in packets:
        ser.write(packet)
    ser.close()




'''


-input validation
-send using struct.pack
-receive data
    

2 ways of setting this up:
    1. Make/generate a list of acceptable values and keep as a global variable. Check if input is in list.
    2. Collection of if statements for each parameter to check for fail-conditions. 
    
'''



def validate(inputList):

    # This function takes in all the inputted parameters (which are strings) and returns 1 iff all paramaters are valid. 
    

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

                


    


# Defining Functions
def readParam():
    # Used to read the parameters stored in the text file
    outList = []

    file1 = open("parameters.txt", "r")
    for line in file1.readlines():
        outList.append(line.strip("\n"))
    file1.close

    return outList

def writeParam(inList):
    # Used to write parameters into the text file
    file1 = open("parameters.txt", "w")

    for line in inList:
        file1.write(str(line) + "\n")

    file1.close()

def checkCreds(name, passwor):
    # Used for checking if a user exits 
    file1 = open("users.txt", "r")
    for line in file1.readlines():
        userCreds.append(line.split())
    file1.close
    
    for cred in userCreds:
        if (cred[0] == name) & (cred[1] == passwor):
            return 1

    return 0

# Setting Up Global Variables 
userCreds = [] # 2D list used for storing all registered usernames and corresponding passowords read from the file. 
device = "0101" # String that stores the device serial number 
comm = 1 # A 1 or 0 used to indicate whether or not the device and DCM are communicating 
pacingModes = ["AOO", "VOO", "AAI", "VVI"] # List that stores all the pacing modes the device can be in 
paramLimits = [(30, 175), (50, 175), (3.5, 7.0), (0.1, 1.9), (3.5, 7.0), (0.1, 1.9), (150, 500), (150, 500)] # List used to store all the bounds for each parameter 

# Populating parameters
parameters = readParam() 

# Window for editing parameters
def editParam():
    
    sg.theme('LightBrown')
    
    layout = [[sg.Text('Leave blank for no change.')],
            [sg.Text("Lower Rate Limit"), sg.Spin(values = (1, 10), initial_value=5, key='-P0-', size=15)],
            [sg.Text("Upper Rate Limit"), sg.InputText(key='-P1-', size=15)],
            [sg.Text("Atrial Amplitude"), sg.InputText(key='-P2-', size=15)],
            [sg.Text("Atrial Pulse Width"), sg.InputText(key='-P3-', size=15)],
            [sg.Text("Ventricular Amplitude"), sg.InputText(key='-P4-', size=15)],
            [sg.Text("Ventricular Pulse Width"), sg.InputText(key='-P5-', size=15)],
            [sg.Text("VRP"), sg.InputText(key='-P6-', size=15)],
            [sg.Text("ARP"), sg.InputText(key='-P7-', size=15)],
            [sg.Button("Submit")],
            [sg.Button('Cancel')]]
    
    window = sg.Window('Edit Parameters', layout)
 
    while True:
        event, values = window.read()
        if event == 'Cancel' or event == sg.WIN_CLOSED:
            window.close()
            dashboard()
            break
        if event == 'Submit':
            
            # Form List of input values
            paramInput = []
            for i in range(0, len(parameters)):
                keyString = "-P" + str(i) + "-"
                paramInput.append(values[keyString])
            
            

            # Checking if values are in range 
            errIn = False
            for i in range(0, len(parameters)):
                keyString = "-P" + str(i) + "-"
                if (values[keyString] != ""):
                    if (paramLimits[i][0] > int(values[keyString]) or int(values[keyString]) > paramLimits[i][1]):
                        errIn = True
                        break
            
            # If the values were in range, the non-blank values are written to file
            if errIn==True:
                sg.popup("Error: Check inputs.")
            else: 
                for i in range(0, len(parameters)):
                    keyString = "-P" + str(i) + "-"
                    if (values[keyString] != ""):
                        parameters[i] = values[keyString]
            
                writeParam(parameters)
                sendParam(parameters)

                window.close()
                dashboard()
                break
        


    window.close()


def commIndicator(key, radius=30):
    # Used to setup the graph for showing the communication indicator
    return sg.Graph(canvas_size=(radius, radius), graph_bottom_left=(-radius, -radius), 
    graph_top_right=(radius, radius), pad=(0, 0), key=key)

def updateIndicator(window, key, color):
    # Used to update the communication indicator
    graph = window[key]
    graph.erase()
    graph.draw_circle((0, 0), 12, fill_color=color, line_color=color)

# Dashboard Window
def dashboard():
    
    sg.theme("LightBrown")

    parameters = readParam()

    layout = [[sg.Text("PACEMAKER Device: " + device)],
            [sg.Text("Device Communication"), commIndicator('-Main-')],
            [sg.Frame("Pacing Mode", [
                [sg.Text(pacingModes[0], font=40, key='-MODE-')]
            ])], 
            [sg.Frame("Parameters", [
                [sg.Text("Lower Rate Limit: " + str(parameters[0]))], 
                [sg.Text("Upper Rate Limit: " + str(parameters[1]))],
                [sg.Text("Atrial Amplitude: " + str(parameters[2]))],
                [sg.Text("Atrial Pulse Width: " + str(parameters[3]))],
                [sg.Text("Ventricular Amplitude: " + str(parameters[4]))],
                [sg.Text("Ventricular Pulse Width: " + str(parameters[5]))],
                [sg.Text("VRP: " + str(parameters[6]))],
                [sg.Text("ARP: " + str(parameters[7]))],
            ])], 
            [sg.Button('Edit Paramaters')],
            [sg.Button('Quit')]]

    window = sg.Window("Dashboard", layout)
    
    i = 0  # used for cycling through the pacing modes for demonstration 
    while True:
        event,values = window.read(timeout=400)
        
        if event == "Quit" or event == sg.WIN_CLOSED:
            break
        if event == "Edit Paramaters":
            window.close()
            editParam()
            break
    
        updateIndicator(window, '-Main-', 'red' if comm==0 else 'green') # On each loop the circle is updated

        # Cycling through pacing modes [FOR DEMO]
        if (i == 3):
            i = 0
        else: 
            i +=1
        window["-MODE-"].update(pacingModes[i])

    window.close()

# Progress Bar Window
def progress_bar():

    sg.theme('LightBrown')

    layout = [[sg.Text('Creating your account...')],
            [sg.ProgressBar(1000, orientation='h', size=(20, 20), key='progbar')],
            [sg.Cancel()]]

    window = sg.Window('Working...', layout)

    # Update the bar for 1000 frames and close window
    for i in range(1000):
        event, values = window.read(timeout=1)
        if event == 'Cancel' or event == sg.WIN_CLOSED:
            break
        window['progbar'].update_bar(i + 1)
    window.close()

# Register a user window
def create_account():

    sg.theme('LightBrown')
    
    layout = [[sg.Text("Sign Up", size =(15, 1), font=40, justification='c')],
             [sg.Text("Create Username", size =(15, 1), font=16), sg.InputText(key='-username-', font=16, size=15)],
             [sg.Text("Create Password", size =(15, 1), font=16), sg.InputText(key='-password-', font=16, password_char='*', size=15)],
             [sg.Button("Submit"), sg.Button("Cancel")]]
 
    window = sg.Window("Sign Up", layout)

    while True:
        event,values = window.read()
        if event == 'Cancel' or event == sg.WIN_CLOSED:
            break
        else:
            if event == "Submit":
                
                # Validating inputs and writing new user to file
                if (" " in values['-username-']) | (" " in values['-password-']) | (values['-password-'] == "") | (values['-username-'] == ""):
                    sg.popup("Invalid input.")
                elif (len(userCreds) < 10) & (checkCreds(values['-username-'], values['-password-']) == 0):
                    
                    # Writing 
                    file1 = open("users.txt", "a")
                    file1.write("\n" + values['-username-'] + " " + values['-password-'])
                    file1.close()

                    progress_bar()
                    window.close()
                    login()
                    break

                else:
                    if (len(userCreds) >= 10):
                        sg.popup("Max users reached.")
                    else:
                        sg.popup("Invalid input.")
                
    window.close()

# Login Screen 
def login():
    sg.theme("LightBrown")

    layout = [[sg.Text("Log In", size =(10, 1), font=40)],
            [sg.Text("Username", size =(10, 1), font=16),sg.InputText(key='-usrnm-', font=16, size=15)],
            [sg.Text("Password", size =(10, 1), font=16),sg.InputText(key='-pwd-', password_char='*', font=16, size=15)],
            [sg.Button('Login'),sg.Button('Register'), sg.Button('Quit')]]

    window = sg.Window("Log In", layout)

    while True:
        event,values = window.read()
        if event == "Quit" or event == sg.WIN_CLOSED:
            break
        else:
            if event == "Login":

                # Validate input and login 
                if (" " in values['-usrnm-']) | (" " in values['-pwd-']) | (values['-pwd-'] == "") | (values['-usrnm-'] == ""):
                    sg.popup("Invalid input.")
                elif (checkCreds(values['-usrnm-'], values['-pwd-'])):
                    window.close()
                    dashboard()
                else:
                    sg.popup("Invalid login. Try again")
                
            if event == "Register":
                window.close()
                create_account()
                

    window.close()

# Greeting screen 
def welcome():
    sg.theme("LightBrown")
    layout = [[sg.Image("heart.png")], 
                [sg.Text("Welcome to the DCM", size=(20), font=40)], 
                [sg.Button('Login')], 
                [sg.Button('Register')], 
                [sg.Button('Quit')]]

    window = sg.Window("Welcome", layout, element_justification='c', text_justification='c')

    while True:
        event, values = window.read()
        if event == "Quit" or event == sg.WIN_CLOSED:
            break
        else:
            if event == 'Login':
                window.close()
                login()
            if event == 'Register':
                window.close()
                create_account()
    window.close()



welcome()

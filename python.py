'''

DEVICE CONTROL MONITOR (DCM)
SFWRENG 3K04 

'''

# input validation 
# param limits

# Importing Libraries 
from textwrap import fill
from tkinter import Event
from tkinter.constants import FALSE
import PySimpleGUI as sg
import random

def readParam():
    outList = []

    file1 = open("parameters.txt", "r")
    for line in file1.readlines():
        outList.append(line.strip("\n"))
    file1.close

    return outList

def writeParam(inList):
    file1 = open("parameters.txt", "w")

    for line in inList:
        file1.write(str(line) + "\n")

    file1.close()

# Setting Up Global Variables 
userCreds = [] # 2D list used for storing all registered usernames and corresponding passowords. 
device = "0101"
comm = 1
pacingModes = ["AOO", "VOO", "AAI", "VVI"]
parameters = readParam()
paramLimits = [(30, 175), (50, 175), (3.5, 7.0), (0.1, 1.9), (3.5, 7.0), (0.1, 1.9), (150, 500), (150, 500)]


def editParam():
    sg.theme('LightBrown')
    layout = [[sg.Text('Leave blank for no change.')],
            [sg.Text("Lower Rate Limit"), sg.InputText(key='-P0-', size=15)],
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
            
            # Checking if values are in range 
            errIn = False
            for i in range(0, len(parameters)):
                keyString = "-P" + str(i) + "-"
                if (values[keyString] != ""):
                    if (paramLimits[i][0] > int(values[keyString]) or int(values[keyString]) > paramLimits[i][1]):
                        errIn = True
                        break

            if errIn==True:
                sg.popup("Error: Check inputs.")
            else: 
                for i in range(0, len(parameters)):
                    keyString = "-P" + str(i) + "-"
                    if (values[keyString] != ""):
                        parameters[i] = values[keyString]
            
                writeParam(parameters)

                window.close()
                dashboard()
                break
        


    window.close()


def commIndicator(key, radius=30):
    return sg.Graph(canvas_size=(radius, radius), graph_bottom_left=(-radius, -radius), 
    graph_top_right=(radius, radius), pad=(0, 0), key=key)

def updateIndicator(window, key, color):
    graph = window[key]
    graph.erase()
    graph.draw_circle((0, 0), 12, fill_color=color, line_color=color)

def dashboard():
    i = 0
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

    while True:
        event,values = window.read(timeout=400)
        
        if event == "Quit" or event == sg.WIN_CLOSED:
            break
        if event == "Edit Paramaters":
            window.close()
            editParam()
            break
    
        updateIndicator(window, '-Main-', 'red' if comm==0 else 'green')    

        if (i == 3):
            i = 0
        else: 
            i +=1

        window["-MODE-"].update(pacingModes[i])

    window.close()


def progress_bar():
    sg.theme('LightBrown')
    layout = [[sg.Text('Creating your account...')],
            [sg.ProgressBar(1000, orientation='h', size=(20, 20), key='progbar')],
            [sg.Cancel()]]

    window = sg.Window('Working...', layout)
    for i in range(1000):
        event, values = window.read(timeout=1)
        if event == 'Cancel' or event == sg.WIN_CLOSED:
            break
        window['progbar'].update_bar(i + 1)
    window.close()


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
                
                file1 = open("users.txt", "a")
                
                if (" " in values['-username-']) | (" " in values['-password-']) | (values['-password-'] == "") | (values['-username-'] == ""):
                    sg.popup("Invalid input.")
                elif (len(userCreds) < 10) & (checkCreds(values['-username-'], values['-password-']) == 0):
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




def checkCreds(name, passwor):

    file1 = open("users.txt", "r")
    for line in file1.readlines():
        userCreds.append(line.split())
    file1.close
    
    for cred in userCreds:
        if (cred[0] == name) & (cred[1] == passwor):
            return 1

    return 0


welcome()

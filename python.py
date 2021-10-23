'''

DEVICE CONTROL MONITOR (DCM)
SFWRENG 3K04 

'''

# TODO: make a input checker function 


# Importing Libraries 
from tkinter import Event
import PySimpleGUI as sg

# Setting Up Global Variables 
userCreds = [] # 2D list used for storing all registered usernames and corresponding passowords. 


def dashboard():
    sg.theme("LightBrown")
    layout = [[sg.Text("Dashboard", size =(15, 1), font=40)],
            [sg.Button('Quit')]]

    window = sg.Window("Dashboard", layout)

    while True:
        event,values = window.read()
        if event == "Quit" or event == sg.WIN_CLOSED:
            break
                

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
             [sg.Text("Create Username", size =(15, 1), font=16), sg.InputText(key='-username-', font=16)],
             [sg.Text("Create Password", size =(15, 1), font=16), sg.InputText(key='-password-', font=16, password_char='*')],
             [sg.Button("Submit"), sg.Button("Cancel")]]
 
    window = sg.Window("Sign Up", layout)

    while True:
        event,values = window.read()
        if event == 'Cancel' or event == sg.WIN_CLOSED:
            break
        else:
            if event == "Submit":
                
                file1 = open("users.txt", "a")
                
                if (len(userCreds) < 10) & (checkCreds(values['-username-'], values['-password-']) == 0):
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
    layout = [[sg.Text("Log In", size =(15, 1), font=40)],
            [sg.Text("Username", size =(15, 1), font=16),sg.InputText(key='-usrnm-', font=16)],
            [sg.Text("Password", size =(15, 1), font=16),sg.InputText(key='-pwd-', password_char='*', font=16)],
            [sg.Button('Login'),sg.Button('Quit'), sg.Button('Register')]]

    window = sg.Window("Log In", layout)

    while True:
        event,values = window.read()
        if event == "Quit" or event == sg.WIN_CLOSED:
            break
        else:
            if event == "Login":
                
                if (checkCreds(values['-usrnm-'], values['-pwd-'])):
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
    print(userCreds)

    for cred in userCreds:
        if (cred[0] == name) & (cred[1] == passwor):
            return 1

    return 0


welcome()

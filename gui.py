'''

gui.py 
Holds all the logic used for the GUI for the DCM. 
Each function represents a state/window. 

'''

# Importing libraries
import PySimpleGUI as sg  
import users

# Setting Global Values for GUI
font = ("Courier New", 10)


# Greeting screen 
def welcome():

    # Setting Theme
    sg.theme("Darkteal11")

    # Defining Layout
    layout = [[sg.Text("WELCOME TO THE DCM", size=(20), font=("Courier New", 12))], 
                [sg.Button('Login')], 
                [sg.Button('Register')], 
                [sg.Button('Quit')],
                [sg.Text("Device Control Monitor v2.0", size=(30,1), font=font)]]

    # Defining Window
    window = sg.Window("Welcome", layout, element_justification='c', text_justification='c', font=font)

    # Event Loop
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
    
    # Close Window 
    window.close()




# Login Screen 
def login():

    # Setting theme
    sg.theme("DarkTeal11")

    # Defining layout 
    layout = [[sg.Text("Log In", size =(10, 1))],
            [sg.Text("Username", size =(10, 1)), sg.InputText(key='-usrnm-',  size=15)],
            [sg.Text("Password", size =(10, 1)), sg.InputText(key='-pwd-', password_char='*',  size=15)],
            [sg.Button('Login'),sg.Button('Register'), sg.Button('Quit')]]

    # Setting up window 
    window = sg.Window("Log In", layout, font=font)

    # Event loop 
    while True:
        event,values = window.read()
        if event == "Quit" or event == sg.WIN_CLOSED:
            break
        else:
            if event == "Login":
                
                if (users.validCreds(values['-usrnm-'], values['-pwd-']) == 0):
                    sg.popup("Invalid input.")
                else:
                    window.close()
                    welcome()
                
            if event == "Register":
                window.close()
                create_account()
                

    window.close()


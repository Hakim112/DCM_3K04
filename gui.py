'''

gui.py 
Holds all the logic used for the GUI for the DCM. 
Each function represents a state/window. 

'''

# Importing libraries
import PySimpleGUI as sg  
import users
import parameters

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
                    dashboard()
                
            if event == "Register":
                window.close()
                create_account()
                

    window.close()




# Register a user window
def create_account():

    # Setting theme
    sg.theme('DarkTeal11')
    
    # Forming layout
    layout = [[sg.Text("Sign Up", size =(15, 1), justification='c')],
             [sg.Text("Create Username", size =(15, 1)), sg.InputText(key='-username-', size=15)],
             [sg.Text("Create Password", size =(15, 1)), sg.InputText(key='-password-', size=15)],
             [sg.Button("Submit"), sg.Button("Cancel")]]
    
    # Defining window
    window = sg.Window("Sign Up", layout, font=font)

    # Event loop
    while True:

        event,values = window.read()
        
        if event == 'Cancel' or event == sg.WIN_CLOSED:
            break
        
        else:
        
            if event == "Submit":
                
                statusCode = users.newUser(values['-username-'], values['-password-'])

                if (statusCode == 0):
                    sg.popup("Invalid input.")
                elif (statusCode == 1):
                    sg.popup("Max users reached.")
                elif (statusCode == 2):
                    sg.popup("User already exists.")
                else:
                    sg.popup("New user added.")
                    window.close()
                    login()
                
    window.close()





# Dashboard Window
def dashboard():
    
    sg.theme("DarkTeal11")

    paramList = parameters.readParam()
    device = "107380"

    layout = [[sg.Text("PACEMAKER Device: " + device)],
            [sg.Text("Device Communication"), commIndicator('-Main-')],
            [sg.Frame("Pacing Mode", [
                [sg.Text(pacingModes[0], font=40, key='-MODE-')]
            ])], 
            [sg.Frame("Parameters", [
                [sg.Text("Lower Rate Limit: " + str(paramList[0]))], 
                [sg.Text("Upper Rate Limit: " + str(paramList[1]))],
                [sg.Text("Atrial Amplitude: " + str(paramList[2]))],
                [sg.Text("Atrial Pulse Width: " + str(paramList[3]))],
                [sg.Text("Ventricular Amplitude: " + str(paramList[4]))],
                [sg.Text("Ventricular Pulse Width: " + str(paramList[5]))],
                [sg.Text("VRP: " + str(paramList[6]))],
                [sg.Text("ARP: " + str(paramList[7]))],
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



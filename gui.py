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
    layout = [[sg.Image("heart3.png")],[sg.Text("WELCOME TO THE DCM", size=(20), font=("Courier New", 14))], 
                [sg.Button('Login')], 
                [sg.Button('Register')], 
                [sg.Button('Quit')],
                [sg.Text("Device Control Monitor v2.0", size=(30,1), font=("Courier New", 9))]]

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
    layout = [[sg.Text("LOG IN", font=("Courier New", 16), size =(10, 1))],
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
    layout = [[sg.Text("REGISTER", font=("Courier New", 16), size =(15, 1))],
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
    
    # Setting Theme
    sg.theme("DarkTeal11")

    # Updating variables
    paramList = parameters.readParam()
    device = "107380"
    comm = 1

    # Defining layout
    layout = [[sg.Text("DASHBOARD", font=("Courier New", 16), size =(10, 1))], [sg.Text("PACEMAKER Device: " + device)],
            [sg.Text("Device Communication: "), commIndicator('-Main-')],
            [sg.Frame("Pacing Mode", [
                [sg.Text(paramList[0], font=("Courier New", 16), key='-MODE-'), sg.Button('Pace Now')]
            ])], 
            [sg.Frame("Parameters", [
                [sg.Text("Lower Rate Limit: ", size=25), sg.Text(str(paramList[1]), background_color='#68868c'), sg.Text("ppm")],
                [sg.Text("Upper Rate Limit: ", size=25), sg.Text(str(paramList[2]), background_color='#68868c'), sg.Text("ppm")],
                [sg.Text("Fixed AV Delay: ", size=25), sg.Text(str(paramList[3]), background_color='#68868c'), sg.Text("ms")],
                [sg.Text("Reaction Time: ", size=25), sg.Text(str(paramList[4]), background_color='#68868c'), sg.Text("sec")],
                [sg.Text("Response Factor: ", size=25), sg.Text(str(paramList[5]), background_color='#68868c'), sg.Text("")],
                [sg.Text("Activity Threshold: ", size=25), sg.Text(str(paramList[6]), background_color='#68868c'), sg.Text("")],
                [sg.Text("Recovery Time: ", size=25), sg.Text(str(paramList[7]), background_color='#68868c'), sg.Text("min")],
                [sg.Text("Maximum Sensor Rate: ", size=25), sg.Text(str(paramList[8]), background_color='#68868c'), sg.Text("ppm")],
                [sg.Text("Atrial Amplitude: ", size=25), sg.Text(str(paramList[9]), background_color='#68868c'), sg.Text("V")],
                [sg.Text("Atrial Pulse Width: ", size=25), sg.Text(str(paramList[10]), background_color='#68868c'), sg.Text("ms")],
                [sg.Text("ARP: ", size=25), sg.Text(str(paramList[11]), background_color='#68868c'), sg.Text("ms")],
                [sg.Text("Atrial Sensitivity: ", size=25), sg.Text(str(paramList[12]), background_color='#68868c'), sg.Text("V")],
                [sg.Text("Ventricular Amplitude: ", size=25), sg.Text(str(paramList[13]), background_color='#68868c'), sg.Text("V")],
                [sg.Text("Ventricular Pulse Width: ", size=25), sg.Text(str(paramList[14]), background_color='#68868c'), sg.Text("ms")],
                [sg.Text("VRP: ", size=25), sg.Text(str(paramList[15]), background_color='#68868c'), sg.Text("ms")],
                [sg.Text("Ventricular Sensitivity: ", size=25), sg.Text(str(paramList[16]), background_color='#68868c'), sg.Text("V")],
                [sg.Button('Edit Paramaters')],
            ])], 
            [sg.Button('Log Out')],
            [sg.Button('Quit')]]

    window = sg.Window("Dashboard", layout, font=font)
    
    while True:
        event,values = window.read(timeout=400)
        
        if event == "Quit" or event == sg.WIN_CLOSED:
            break

        if event == "Pace Now":

            # parameters.sendParam(paramList) 

            if(parameters.validateSend(paramList)):
                comm = 1
                sg.popup("Parameters sent successfully.")
            else:
                comm = 0
                sg.popup("Unsuccesfull send. Try again.")
            

        if event == "Edit Paramaters":
            window.close()
            editParam()
            break

        if event == "Log Out":
            window.close()
            welcome()
            break
    
        updateIndicator(window, '-Main-', 'red' if comm==0 else 'green') # On each loop the circle is updated

    window.close()






# Window for editing parameters
def editParam():
    
    sg.theme('DarkTeal11')
    
    paramList = parameters.readParam()


    modeSelection = ["AOO", "VOO", "AAI", "VVI", "DOO", "DOOR", "AOOR", "VOOR", "AAIR", "VVIR"]
    # modeSelection = ["DDD", "DDI", "DOO", "AOO", "AAI", "VOO", "VVI", "AAT", "VVT", "DDDR", "VDDR", "DDIR", "DOOR", "AOOR", "AAIR", "VOOR", "VVIR"]
    actThresSelection = ["V-Low", "Low", "Med-Low", "Med", "Med-High", "High", "V-High"]
    avUnregSelection = ["0", "1.25", "2.5", "3.75", "5.0"]

    layout = [[sg.Text('Leave blank for no change. Put 0 for Off.')],
            [sg.Text("Pacing Mode", size=25), sg.Combo(modeSelection, key='-P0-')],
            [sg.Text("Lower Rate Limit", size=25), sg.InputText(key='-P1-', size=15)],
            [sg.Text("Upper Rate Limit", size=25), sg.InputText(key='-P2-', size=15)],
            [sg.Text("Fixed AV Delay", size=25), sg.InputText(key='-P3-', size=15)],
            [sg.Text("Reaction Time", size=25), sg.InputText(key='-P4-', size=15)],
            [sg.Text("Response Factor", size=25), sg.InputText(key='-P5-', size=15)],
            [sg.Text("Activity Threshold", size=25), sg.Combo(actThresSelection, key='-P6-')],
            [sg.Text("Recovery Time", size=25), sg.InputText(key='-P7-', size=15)],
            [sg.Text("Maximum Sensor Rate", size=25), sg.InputText(key='-P8-', size=15)],
            [sg.Text("Atrial Amplitude", size=25), sg.Combo(avUnregSelection, key='-P9-', size=15)],
            [sg.Text("Atrial Pulse Width", size=25), sg.InputText(key='-P10-', size=15)],
            [sg.Text("ARP", size=25), sg.InputText(key='-P11-', size=15)],
            [sg.Text("Atrial Sensitivity", size=25), sg.InputText(key='-P12-', size=15)],
            [sg.Text("Ventricular Amplitude", size=25), sg.Combo(avUnregSelection, key='-P13-', size=15)],
            [sg.Text("Ventricular Pulse Width", size=25), sg.InputText(key='-P14-', size=15)],
            [sg.Text("VRP", size=25), sg.InputText(key='-P15-', size=15)],
            [sg.Text("Ventricular Sensitivity", size=25), sg.InputText(key='-P16-', size=15)],
            [sg.Button("Submit"), sg.Button('Set Nominal'), sg.Button('Cancel')]]
    
    window = sg.Window('Edit Parameters', layout, font=font)
 
    while True:
        event, values = window.read()
        if event == 'Cancel' or event == sg.WIN_CLOSED:
            window.close()
            dashboard()
            break
        if event == 'Submit':
            
            # Form List of input values
            paramInput = []
            for i in range(0, len(paramList)):
                keyString = "-P" + str(i) + "-"
                paramInput.append(values[keyString])
            print(paramInput)
            
            # Input valid
            validation = parameters.validate(paramInput)
            if ("0" not in validation):
                parameters.writeParam(paramInput)
                window.close()
                dashboard()
                break
            else:
                sg.popup("Invalid Input")
        
        if event == 'Set Nominal':
            paramInput = ['AOO', '60', '120', '150', '30', '8', 'Med', '5', '120', '3.75', '1', '250', '2.5', '3.75', '1', '320', '2.5']
            parameters.writeParam(paramInput)
            window.close()
            dashboard()
            break

    window.close()



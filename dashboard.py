
import PySimpleGUI as sg  
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

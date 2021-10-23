import PySimpleGUI as sg


username = ''
password = ''

userCreds = []



def progress_bar():
    sg.theme('LightBlue2')
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
    global username, password
    sg.theme('LightBlue2')
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
    global username,password
    sg.theme("LightBlue2")
    layout = [[sg.Text("Log In", size =(15, 1), font=40)],
            [sg.Text("Username", size =(15, 1), font=16),sg.InputText(key='-usrnm-', font=16)],
            [sg.Text("Password", size =(15, 1), font=16),sg.InputText(key='-pwd-', password_char='*', font=16)],
            [sg.Button('Ok'),sg.Button('Cancel'), sg.Button('Register')]]

    window = sg.Window("Log In", layout)

    while True:
        event,values = window.read()
        if event == "Cancel" or event == sg.WIN_CLOSED:
            break
        else:
            if event == "Ok":
                
                if (checkCreds(values['-usrnm-'], values['-pwd-'])):
                    sg.popup("Welcome!")
                else:
                    sg.popup("Invalid login. Try again")
                
            if event == "Register":
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


# TODO: make a input checker function 

login()


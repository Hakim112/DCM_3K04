'''

users.py 
This module holds all fucntions and logic related to users. 

'''



def validCreds(user, pswr):
    # Used for checking if a user exits 

    if (validInput(user, pswr) == 0):
        return 0
    else:

        userCreds = []

        file1 = open("users.txt", "r")
        for line in file1.readlines():
            userCreds.append(line.split())
        file1.close

        for cred in userCreds:
            if (cred[0] == user) & (cred[1] == pswr):
                return 1

        return 0

def validInput(user, pswr):
    return not((" " in user) | (" " in pswr) | (pswr == "") | (user == ""))


def newUser(user, pswr):

    if (validInput(user, pswr) == 0):
        return 0
    else: 
        
        # Read users
        userCreds = []
        file1 = open("users.txt", "r")
        for line in file1.readlines():
            userCreds.append(line.split())
        file1.close
        
        # Max users reached
        if (len(userCreds) >= 10):
            return 1
        # User already exists
        elif (validCreds(user, pswr)):
            return 2
        else:
            file1 = open("users.txt", "a")
            file1.write("\n" + user + " " + pswr)
            file1.close()
            return 3








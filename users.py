'''

users.py 
This module holds all fucntions and logic related to users. 

'''
import os


def validCreds(user, pswr):
    # Used for checking if a user exits 
    cwd = os.getcwd()
    print(cwd)
    print(os.listdir(cwd))

    # if ((" " in user) | (" " in pswr) | (pswr == "") | (user == "")):
    #     return 0
    # else:
# 
    #     userCreds = []
# 
    #     file1 = open("users.txt", "r")
    #     for line in file1.readlines():
    #         userCreds.append(line.split())
    #     file1.close
# 
    #     for cred in userCreds:
    #         if (cred[0] == user) & (cred[1] == pswr):
    #             return 1
# 
    #     return 0



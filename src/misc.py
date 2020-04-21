import os
import sys
import json
import string
import random
import colorama
from colorama import Fore, Style

def ePrint(msg):
    print(Fore.RED + Style.BRIGHT + 'Error: ' + msg + Style.RESET_ALL)
    
def sPrint(msg):
    print(Fore.GREEN + Style.BRIGHT + 'Success: ' + msg + Style.RESET_ALL)

def random_alphaNumeric_string(lettersCount, digitsCount):
    sampleStr = ''.join((random.choice(string.ascii_letters) for i in range(lettersCount)))
    sampleStr += ''.join((random.choice(string.digits) for i in range(digitsCount)))
    sampleList = list(sampleStr)
    random.shuffle(sampleList)
    finalString = ''.join(sampleList)
    return finalString

def isFileExist(file):
    if not os.path.isfile(file): 
        ePrint("No such file : " + file)
        exit(1)
    return True
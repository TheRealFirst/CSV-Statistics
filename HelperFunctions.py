import os
from Data import Data

def isCSV(fileName):
    file, fileExtension = os.path.splitext(fileName)
    if fileExtension != ".csv" and fileExtension != ".CSV":
            return False
    return True

def CalculateSum(data, roundTo=None):
    sum = 0
    for i in range(len(data.values)):
        sum += data.values[i]
    if(roundTo):
         sum = round(sum, roundTo)
    return sum

def GetFirstAndLastPosition(data):
    firstPos = -1
    lastPos = -1

    if len(data.time) != len(data.values):
        print("Time and Values werent the same length")
        return False

    for i in range(len(data.time)):
        if data.values[i] != 0:
            firstPos = i
            break
        
    for j in range(len(data.time) - 1, -1, -1):
        if data.values[j] != 0:
            lastPos = j
            break
        
    
    return firstPos, lastPos

def isEven(number):
    if number%2 == 0:
        return 1
    return 0
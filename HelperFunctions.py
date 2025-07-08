import os
from Data import Data
from enum import Enum


class ListModifications(Enum):
    Option1 = "No Modification"
    Option2 = "Denoise"
    Option3 = "Denoise + Cut Ends"

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

def GetFirstAndLastPosition(data): # rewrite to just set the values
    firstPos = -1
    lastPos = -1

    if len(data.time) != len(data.values):
        print("Time and Values werent the same length")
        return False

    for i in range(len(data.time)):
        if data.values[i] != 0:
            firstPos = i
            print(i)
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

def cleanUpDataSet(data, listModification,noiseThreshold=0.0):
    del data.values[0] # Delete Headers
    del data.time[0] # Delete Headers

    for i in range(len(data.values)): # Switches nan to zero
        if data.values[i] == "nan":
            data.values[i] = 0


    convertListToInt(data)

    data.firstPos, data.lastPos = GetFirstAndLastPosition(data)

    data.originalTime = data.time
    data.originalValues = data.values

    if noiseThreshold > 0: #delete noise under Threshold
        i = data.firstPos
        while i <= data.lastPos:
            if data.values[i] == 0:
                del data.values[i]
                del data.time[i]
                data.lastPos -= 1
            else:
                i += 1
    
    
    data.denoisedTime= data.time
    data.denoisedValues = data.values

    print(data.values)

    while 0 < data.firstPos:
        del data.time[0]
        del data.values[0]
        data.firstPos -= 1
        data.lastPos -= 1

    while len(data.values) > data.lastPos:
        del data.time[-1]
        del data.values[-1]
    
    
    data.fullyCleanedTime = data.time
    data.fullyCleanedValues = data.values

    if listModification == ListModifications.Option1.value:
        data.time = data.originalTime
        data.values = data.originalValues
    elif listModification == ListModifications.Option2.value:
        data.time = data.denoisedTime
        data.values = data.denoisedValues
    else:
        pass

    data.firstPos, data.lastPos = GetFirstAndLastPosition(data)

    
    

def convertListToInt(data):
        data.time = list(map(float, data.time))
        data.values = list(map(float, data.values))
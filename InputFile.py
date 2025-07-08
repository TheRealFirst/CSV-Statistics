from tkinter import StringVar
import numpy
import matplotlib.pyplot as plt
import csv
from sklearn.metrics import r2_score

from HelperFunctions import CalculateSum, GetFirstAndLastPosition, ListModifications, cleanUpDataSet, convertListToInt, isCSV
import Data

class InputFile():
    def __init__(self, fileName, listModifications):
        self.data = Data.Data()
        self.fileName = fileName
        self.roundTo = 2
        self.polyDeg = 3
        self.r2String = StringVar()
        self.degString = StringVar()
        self.integString = StringVar()
        self.currentListMod = listModifications
        self.loadFile(fileName)
        self.AnalyzeData()

    def loadFile(self, fileName):
        if not isCSV(fileName):
            print("Couldnt load file: " + fileName + ", because is no csv!")
            return False

        with open(fileName,'r') as csvfile:
            lines = csv.reader(csvfile, delimiter=',')
            for row in lines:
                self.data.time.append(row[0])
                self.data.values.append(row[1])

        cleanUpDataSet(self.data, self.currentListMod, 0.01)
        print("First Pos: " + str(self.data.firstPos))
        print("Last Pos: " + str(self.data.lastPos))

    def OnListModChange(self, newListMod):
        if newListMod == ListModifications.Option1.value:
            self.data.time = self.data.originalTime
            self.data.values = self.data.originalValues
        elif newListMod == ListModifications.Option2.value:
            self.data.time = self.data.denoisedTime
            self.data.values = self.data.denoisedValues
        else:
            self.data.time = self.data.fullyCleanedTime
            self.data.values = self.data.fullyCleanedValues

        self.data.firstPos, self.data.lastPos = GetFirstAndLastPosition(self.data)
        self.AnalyzeData()
        


    def AnalyzeData(self):
        self.data.sum = CalculateSum(self.data, self.roundTo)
        self.data.max = max(self.data.values)
        self.data.firstPos, self.data.lastPos = GetFirstAndLastPosition(self.data)
        self.data.mesuredTime = self.data.time[self.data.lastPos] - self.data.time[self.data.firstPos]
        self.CalculatePolynom(self.polyDeg)

    def PolyDegUp(self):
        self.polyDeg += 1
        self.CalculatePolynom(self.polyDeg)
    
    def PolyDegDown(self):
        self.polyDeg -= 1
        self.CalculatePolynom(self.polyDeg)


    def CalculatePolynom(self, deg):
        self.poly = numpy.polyfit(self.data.time, self.data.values, deg)
        self.model = numpy.poly1d(self.poly)
        self.line = numpy.linspace(0, self.data.time[-1])
        self.r2 = r2_score(self.data.values, self.model(self.data.time))
        self.r2String.set("r2: " + str(self.r2))
        self.degString.set("Degree: " + str(self.polyDeg))
        area = numpy.polyint(self.model)
        self.integral = area(self.data.lastPos) - area(self.data.firstPos)
        self.integString.set("Integral: " + str(self.integral))

    def DrawPlot(self):

        plt.scatter(self.data.time, self.data.values, color = 'g',s = 10)
        plt.plot(self.line, self.model(self.line))
        plt.xticks(rotation = 25)
        plt.xlabel('Time')
        plt.ylabel('Values')
        plt.title('Light Strength', fontsize = 20)

        plt.show()

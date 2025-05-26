import matplotlib.pyplot as plt
import csv

from HelperFunctions import CalculateSum, GetFirstAndLastPosition, isCSV
import Data

class InputFile():
    def __init__(self, fileName):
        self.data = Data.Data()
        self.fileName = fileName
        self.roundTo = 2
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

        del self.data.values[0]
        del self.data.time[0]
        for i in range(len(self.data.values)):
            if self.data.values[i] == "nan":
                self.data.values[i] = 0

        
        self.data.time = list(map(float, self.data.time))
        self.data.values = list(map(float, self.data.values))

    def AnalyzeData(self):
        self.data.sum = CalculateSum(self.data, self.roundTo)
        self.data.max = max(self.data.values)
        self.data.firstPos, self.data.lastPos = GetFirstAndLastPosition(self.data)
        self.data.mesuredTime = self.data.time[self.data.lastPos] - self.data.time[self.data.firstPos]

    def DrawPlot(self):
        plt.scatter(self.data.time, self.data.values, color = 'g',s = 10)
        plt.xticks(rotation = 25)
        plt.xlabel('Time')
        plt.ylabel('Values')
        plt.title('Light Strength', fontsize = 20)

        plt.show()

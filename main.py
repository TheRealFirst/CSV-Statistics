import matplotlib.pyplot as plt
import csv
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilenames
import os

def isCSV(fileName):
    file, fileExtension = os.path.splitext(fileName)
    if fileExtension != ".csv" and fileExtension != ".CSV":
            return False
    return True

class InputFile():
    def __init__(self, fileName):
        self.time = []
        self.values = []
        self.fileName = fileName
        self.loadFile(fileName)

    def loadFile(self, fileName):
        if not isCSV(fileName):
            print("Couldnt load file: " + fileName + ", because is no csv!")
            return False

        with open(fileName,'r') as csvfile:
            lines = csv.reader(csvfile, delimiter=',')
            for row in lines:
                self.time.append(row[0])
                self.values.append(row[1])

        del self.values[0]
        del self.time[0]
        for i in range(len(self.values)):
            if self.values[i] == "nan":
                self.values[i] = 0

    def DrawPlot(self):
        plt.scatter(self.time, self.values, color = 'g',s = 10)
        plt.xticks(rotation = 25)
        plt.xlabel('Time')
        plt.ylabel('Values')
        plt.title('Light Strength', fontsize = 20)

        plt.show()

files = []
def loadFile():
    filenames = askopenfilenames()
    if filenames:
        for filename in filenames:
            if(isCSV(filename)):
                file = InputFile(filename)
                files.append(file)

                show_button = ttk.Button(frm, text=f"Show Graph: {os.path.basename(file.fileName)}", command=file.DrawPlot)
                show_button.pack(pady=5)
    
    
root = Tk()
frm = ttk.Frame(root, padding=10)
frm.pack()
ttk.Button(frm, text="load file", command=loadFile).pack()
ttk.Button(frm, text="Quit", command=root.destroy).pack()
root.mainloop()
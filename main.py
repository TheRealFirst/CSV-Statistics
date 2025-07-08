
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilenames
from tkinter.filedialog import asksaveasfilename
import os
import math

from HelperFunctions import ListModifications, isCSV, isEven
from InputFile import InputFile

root = Tk()

def filePanel(file):
    frm = ttk.Frame(root, padding=10, relief="solid", borderwidth=1)
    frm.grid(row=math.ceil(len(files) / 2), column=isEven(len(files)), sticky="ew", padx=5, pady=5)

    show_button = ttk.Button(frm, text=f"Show Graph: {os.path.basename(file.fileName)}", command=file.DrawPlot)
    show_button.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

    sum = ttk.Label(frm, text="Sum: " + str(file.data.sum)).grid()
    max = ttk.Label(frm, text="Max: " + str(file.data.max)).grid()
    Time = ttk.Label(frm, text="Time: " + str(file.data.mesuredTime)).grid()
    integral = ttk.Label(frm, textvariable=file.integString).grid()
    regLabel = ttk.Label(frm, text="Polynomical Regression").grid()
    regLabel2 = ttk.Label(frm, textvariable=file.degString).grid()
    polyDegUp = ttk.Button(frm, text="Increase", command=file.PolyDegUp).grid()
    polyDegDown = ttk.Button(frm, text="Decrease", command=file.PolyDegDown).grid()
    r2 = ttk.Label(frm, textvariable=file.r2String).grid()

files = []
currentModification = StringVar(value=ListModifications.Option2.value)

def loadFile():
    filenames = askopenfilenames()
    if filenames:
        for filename in filenames:
            if isCSV(filename):
                file = InputFile(filename, currentModification.get())
                files.append(file)
                filePanel(file)

def saveFile():
    pass

def OnListModChange():
    for file in files:
        file.OnListModChange(currentModification.get())


root.geometry("640x360")
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Button(frm, text="load file", command=loadFile).grid(column=0, row=0)
ttk.Button(frm, text="Save", command=saveFile).grid(column=1, row=0)
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=2, row=0)

options = list(ListModifications)
ttk.OptionMenu(frm, currentModification, options[1].value, *[opt.value for opt in options]).grid(column=3, row=0)
currentModification.trace_add("write", OnListModChange)

root.mainloop()
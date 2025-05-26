
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilenames
from tkinter.filedialog import asksaveasfilename
import os
import math

from HelperFunctions import isCSV, isEven
from InputFile import InputFile


def filePanel(file):
    frm = ttk.Frame(root, padding=10, relief="solid", borderwidth=1)
    frm.grid(row=math.ceil(len(files) / 2), column=isEven(len(files)), sticky="ew", padx=5, pady=5)

    show_button = ttk.Button(frm, text=f"Show Graph: {os.path.basename(file.fileName)}", command=file.DrawPlot)
    show_button.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

    sum = ttk.Label(frm, text="Sum: " + str(file.data.sum)).grid()
    max = ttk.Label(frm, text="Max: " + str(file.data.max)).grid()
    Time = ttk.Label(frm, text="Time: " + str(file.data.mesuredTime)).grid()

files = []

def loadFile():
    filenames = askopenfilenames()
    if filenames:
        for filename in filenames:
            if isCSV(filename):
                file = InputFile(filename)
                files.append(file)
                filePanel(file)

def saveFile():
    pass

root = Tk()
root.geometry("640x360")
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Button(frm, text="load file", command=loadFile).grid(column=0, row=0)
ttk.Button(frm, text="Save", command=saveFile).grid(column=1, row=0)
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=2, row=0)
root.mainloop()
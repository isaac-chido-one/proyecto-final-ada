import tkinter as tk
from tkinter import ttk
from utils import appName

class Menu(tk.Tk):
    def __init__(self, sourceFile):
        super().__init__()
        #loadStructures(sourceFile)
        self.modalStock = None
        self.modalPos = None

        self.geometry('800x600')
        self.title(appName() + ' - Home')
        self.resizable(True, True)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # frame
        self.frame = tk.Frame(self)
        self.frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.frame.rowconfigure(0, weight=11)
        self.frame.rowconfigure(1, weight=1)
        self.frame.columnconfigure(0, weight=2)
        self.frame.columnconfigure(1, weight=3)
        self.frame.columnconfigure(2, weight=2)
        self.frame.columnconfigure(3, weight=3)
        self.frame.columnconfigure(4, weight=2)

        # author label
        self.labelAuthor = ttk.Label(self.frame, text='Powered by: Perla Dueñas, Herón Ortiz & Isaac Rojas')
        self.labelAuthor.grid(column=3, row=1, columnspan=2, sticky=tk.SE)

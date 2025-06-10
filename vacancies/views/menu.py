import tkinter as tk
from tkfontawesome import icon_to_image
from tkinter import ttk
from vacancies.utils import appName
from vacancies.views.table_applicants import TableApplicants
from vacancies.views.table_vacancies import TableVacancies

class Menu(tk.Tk):
    ''' Ventana principal '''

    def __init__(self):
        ''' Agrgega los widgets necesarios a la ventana. '''
        super().__init__()
        self.modalApplicants = TableApplicants(self)
        self.modalVacancies = TableVacancies(self)

        self.geometry('800x600')
        self.title(appName('Home'))
        self.resizable(True, True)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # styling
        self.style = ttk.Style()
        self.style.configure('PFADA.TButton', background='white', foreground='#4267b2', padding=5, font='helvetica 24')

        # frame
        self.frame = tk.Frame(self)
        self.frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.frame.rowconfigure(0, weight=11)
        self.frame.rowconfigure(1, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=3)
        self.frame.columnconfigure(2, weight=1)
        self.frame.columnconfigure(3, weight=3)
        self.frame.columnconfigure(4, weight=1)

        # vacancies button
        self.iconVacancies = icon_to_image('suitcase', fill="#4267B2", scale_to_width=64)
        self.buttonVacancies = ttk.Button(self.frame, text='Vacantes', style='PFADA.TButton', image=self.iconVacancies, compound=tk.BOTTOM, command=lambda: self.openModalVacancies())
        self.buttonVacancies.grid(column=1, row=0, sticky=tk.EW)

        # applicants button
        self.iconApplicants = icon_to_image('user-tie', fill="#4267B2", scale_to_width=64)
        self.buttonApplicants = ttk.Button(self.frame, text='Candidatos', style='PFADA.TButton', image=self.iconApplicants, compound=tk.BOTTOM, command=lambda: self.openModalApplicants())
        self.buttonApplicants.grid(column=3, row=0, sticky=tk.EW)

        # author label
        self.labelAuthor = ttk.Label(self.frame, text='Powered by: Perla Dueñas, Herón Ortiz & Isaac Rojas')
        self.labelAuthor.grid(column=0, row=1, columnspan=6, sticky=tk.SE)

    def openModalApplicants(self):
        ''' Abre la ventana de candidatos '''
        self.modalApplicants.open()

    def openModalVacancies(self):
        ''' Abre la ventana de vacantes '''
        self.modalVacancies.open()

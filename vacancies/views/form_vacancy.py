import re
import tkinter as tk
#from fruit_store.fruits import *
from tkfontawesome import icon_to_image
from tkinter import filedialog
from tkinter import ttk
from vacancies.utils import appName

class FormVacancy(tk.Toplevel):

    def __init__(self, parentModal):
        super().__init__(parentModal)

        self.title(appName() + ' - Vacante')
        self.geometry("800x400")
        self.state('withdrawn')
        self.protocol('WM_DELETE_WINDOW', self.onClose)

        # configure the grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=1)

        # title
        self.iconTitle = icon_to_image('sitemap', fill="#4267B2", scale_to_width=16)
        self.labelTitle = ttk.Label(self, text="Puesto:", image=self.iconTitle, compound=tk.LEFT)
        self.labelTitle.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
        self.entryTitle = ttk.Entry(self)
        self.entryTitle.grid(column=1, row=0, sticky=tk.EW, padx=5, pady=5)

        # company
        self.iconCompany = icon_to_image('industry', fill="#4267B2", scale_to_width=16)
        self.labelCompany = ttk.Label(self, text="Empresa:", image=self.iconCompany, compound=tk.LEFT)
        self.labelCompany.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
        self.entryCompany = ttk.Entry(self)
        self.entryCompany.grid(column=1, row=1, sticky=tk.EW, padx=5, pady=5)

        # location
        self.iconLocation = icon_to_image('location-dot', fill="#4267B2", scale_to_width=16)
        self.labelLocation = ttk.Label(self, text="Locación:", image=self.iconLocation, compound=tk.LEFT)
        self.labelLocation.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)
        self.entryLocation = ttk.Entry(self)
        self.entryLocation.grid(column=1, row=2, sticky=tk.EW, padx=5, pady=5)

        # min salary
        self.iconMinSalary = icon_to_image('dollar-sign', fill="#4267B2", scale_to_width=16)
        self.labelMinSalary = ttk.Label(self, text="Salario mínimo:", image=self.iconMinSalary, compound=tk.LEFT)
        self.labelMinSalary.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)
        self.entryMinSalary = ttk.Entry(self)
        self.entryMinSalary.grid(column=1, row=3, sticky=tk.EW, padx=5, pady=5)

        # max salary
        self.iconMaxSalary = icon_to_image('dollar-sign', fill="#4267B2", scale_to_width=16)
        self.labelMaxSalary = ttk.Label(self, text="Salario máximo:", image=self.iconMaxSalary, compound=tk.LEFT)
        self.labelMaxSalary.grid(column=0, row=4, sticky=tk.W, padx=5, pady=5)
        self.entryMaxSalary = ttk.Entry(self)
        self.entryMaxSalary.grid(column=1, row=4, sticky=tk.EW, padx=5, pady=5)

        # description
        self.iconDescription = icon_to_image('list-ul', fill="#4267B2", scale_to_width=16)
        self.labelDescription = ttk.Label(self, text="Descripción:", image=self.iconDescription, compound=tk.LEFT)
        self.labelDescription.grid(column=0, row=5, sticky=tk.W, padx=5, pady=5)
        self.textDescription = tk.Text(self, height=4, width=80)
        self.textDescription.grid(column=1, row=5, sticky=tk.EW, padx=5, pady=5)

        # requirements
        self.iconRequirements = icon_to_image('list-check', fill="#4267B2", scale_to_width=16)
        self.labelRequirements = ttk.Label(self, text="Requisitos:", image=self.iconRequirements, compound=tk.LEFT)
        self.labelRequirements.grid(column=0, row=6, sticky=tk.W, padx=5, pady=5)
        self.textRequirements = tk.Text(self, height=4, width=80)
        self.textRequirements.grid(column=1, row=6, sticky=tk.EW, padx=5, pady=5)

        # buttons frame
        self.frameButtons = tk.Frame(self)
        self.frameButtons.grid(row=7, column=1, columnspan=2, sticky=tk.E, pady=10)
        self.frameButtons.rowconfigure(0, weight=1)
        self.frameButtons.rowconfigure(1, weight=1)
        self.frameButtons.columnconfigure(0, weight=1)

        # cancel button
        self.iconCancel = icon_to_image('times', fill="#4267B2", scale_to_width=16)
        self.buttonCancel = ttk.Button(self.frameButtons, text='Cancelar', image=self.iconCancel, compound=tk.LEFT, command=lambda: self.close())
        self.buttonCancel.grid(column=0, row=0, padx=5)

        # accept button
        self.iconStore = icon_to_image('check', fill="#4267B2", scale_to_width=16)
        self.buttonStore = ttk.Button(self.frameButtons, text='Guardar', image=self.iconStore, compound=tk.LEFT, command=lambda: self.save())
        self.buttonStore.grid(column=1, row=0, padx=5)

    # Evento al cerrar la ventana
    def onClose(self):
        self.close()

    # Abrir la ventana
    def open(self, callbackOnStore = None):
        self.entryTitle.delete(0, tk.END)
        self.entryCompany.delete(0, tk.END)
        self.entryLocation.delete(0, tk.END)
        self.entryMaxSalary.delete(0, tk.END)
        self.iconify()

        self.code = code
        self.callbackOnStore = callbackOnStore

    # Cerrar la ventana
    def close(self):
        self.withdraw()

    # Guadar la información de una fruta
    def save(self):
        code = self.entryTitle.get()
        code = code.strip()
        item = self.entryCompany.get()
        item = item.strip()
        cost = self.entryLocation.get()
        cost = cost.strip()
        image = self.entryMaxSalary.get()

        # validar código
        if code == '':
            notifyAlert('El código es requerido', self.entryTitle)
            return
        if (code is None or code != self.code) and existsFruit(code):
            notifyAlert('El código ya está asignado a otro artículo', self.entryTitle)
            return

        # validar fruta
        if item == '':
            notifyAlert('El artículo es requerido', self.entryCompany)
            return

        # validar costo
        if cost == '':
            notifyAlert('El costo es requerido', self.entryLocation)
            return
        if re.match(r'^[\-\+]?\d+(\.\d*)?$', cost) is None:
            notifyAlert('El costo debe ser un valor numérico', self.entryLocation)
            return

        cost = float(cost)

        if image == '':
            image = None

        self.close()
        self.callbackOnStore(code, item, cost, image)

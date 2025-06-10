import re
import tkinter as tk
from tkinter import ttk
from typing import Callable
from vacancies.entities.vacancy import Vacancy
from vacancies.structures.app import findVacancy, insertVacancy
from vacancies.utils import appName, createIcon, notifyAlert, notifySuccess

class FormVacancy(tk.Toplevel):
    ''' Ventana de creación o edición de vcacantes. '''

    def __init__(self, parentModal: tk.Toplevel, callback: Callable[[], None]):
        ''' Agrgega los widgets necesarios a la ventana. '''
        super().__init__(parentModal)
        self.callback = callback
        self.vacancy = Vacancy()

        self.title(appName('Vacantes'))
        self.geometry('800x400')
        self.state('withdrawn')
        self.protocol('WM_DELETE_WINDOW', self.close)

        # configure the grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        # title
        self.iconTitle = createIcon('sitemap')
        self.labelTitle = ttk.Label(self, text='Puesto: *', image=self.iconTitle, compound=tk.LEFT)
        self.labelTitle.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
        self.entryTitle = ttk.Entry(self)
        self.entryTitle.grid(column=1, row=0, sticky=tk.EW, padx=5, pady=5)

        # company
        self.iconCompany = createIcon('industry')
        self.labelCompany = ttk.Label(self, text='Empresa: *', image=self.iconCompany, compound=tk.LEFT)
        self.labelCompany.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
        self.entryCompany = ttk.Entry(self)
        self.entryCompany.grid(column=1, row=1, sticky=tk.EW, padx=5, pady=5)

        # location
        self.iconLocation = createIcon('location-dot')
        self.labelLocation = ttk.Label(self, text='Locación: *', image=self.iconLocation, compound=tk.LEFT)
        self.labelLocation.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)
        self.entryLocation = ttk.Entry(self)
        self.entryLocation.grid(column=1, row=2, sticky=tk.EW, padx=5, pady=5)

        # min salary
        self.iconMinSalary = createIcon('dollar-sign')
        self.labelMinSalary = ttk.Label(self, text='Salario mínimo:', image=self.iconMinSalary, compound=tk.LEFT)
        self.labelMinSalary.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)
        self.entryMinSalary = ttk.Entry(self)
        self.entryMinSalary.grid(column=1, row=3, sticky=tk.EW, padx=5, pady=5)

        # max salary
        self.iconMaxSalary = createIcon('dollar-sign')
        self.labelMaxSalary = ttk.Label(self, text='Salario máximo:', image=self.iconMaxSalary, compound=tk.LEFT)
        self.labelMaxSalary.grid(column=0, row=4, sticky=tk.W, padx=5, pady=5)
        self.entryMaxSalary = ttk.Entry(self)
        self.entryMaxSalary.grid(column=1, row=4, sticky=tk.EW, padx=5, pady=5)

        # description
        self.iconDescription = createIcon('list-ul')
        self.labelDescription = ttk.Label(self, text='Descripción:', image=self.iconDescription, compound=tk.LEFT)
        self.labelDescription.grid(column=0, row=5, sticky=tk.W, padx=5, pady=5)
        self.textDescription = tk.Text(self, height=4, width=80)
        self.textDescription.grid(column=1, row=5, sticky=tk.EW, padx=5, pady=5)

        # requirements
        self.iconRequirements = createIcon('list-check')
        self.labelRequirements = ttk.Label(self, text='Requisitos:', image=self.iconRequirements, compound=tk.LEFT)
        self.labelRequirements.grid(column=0, row=6, sticky=tk.W, padx=5, pady=5)
        self.textRequirements = tk.Text(self, height=4, width=80)
        self.textRequirements.grid(column=1, row=6, sticky=tk.EW, padx=5, pady=5)

        # buttons frame
        self.frameButtons = tk.Frame(self)
        self.frameButtons.grid(row=7, column=0, columnspan=2, sticky=tk.E, pady=10)
        self.frameButtons.rowconfigure(0, weight=1)
        self.frameButtons.rowconfigure(1, weight=1)
        self.frameButtons.columnconfigure(0, weight=1)

        # cancel button
        self.iconCancel = createIcon('times')
        self.buttonCancel = ttk.Button(self.frameButtons, text='Cancelar', image=self.iconCancel, compound=tk.LEFT, command=lambda: self.close())
        self.buttonCancel.grid(column=0, row=0, padx=5)

        # accept button
        self.iconStore = createIcon('check')
        self.buttonStore = ttk.Button(self.frameButtons, text='Guardar', image=self.iconStore, compound=tk.LEFT, command=lambda: self.store())
        self.buttonStore.grid(column=1, row=0, padx=5)

    def open(self, vacancy = None):
        ''' Abrir la ventana '''
        self.vacancy = vacancy
        self.entryTitle.delete(0, tk.END)
        self.entryCompany.delete(0, tk.END)
        self.entryLocation.delete(0, tk.END)
        self.entryMinSalary.delete(0, tk.END)
        self.entryMaxSalary.delete(0, tk.END)
        self.textDescription.delete('1.0', tk.END)
        self.textRequirements.delete('1.0', tk.END)

        if not vacancy is None:
            self.entryTitle.insert(0, vacancy.title)
            self.entryCompany.insert(0, vacancy.company)
            self.entryLocation.insert(0, vacancy.location)
            self.entryMinSalary.insert(0, '' if vacancy.min_salary is None else '{0:,.2f}'.format(vacancy.min_salary))
            self.entryMaxSalary.insert(0, '' if vacancy.max_salary is None else '{0:,.2f}'.format(vacancy.max_salary))
            self.textDescription.insert('1.0', vacancy.description)
            self.textRequirements.insert('1.0', vacancy.requirements)

        self.iconify()

    def close(self):
        ''' Cerrar la ventana '''
        self.withdraw()
        self.callback()

    def store(self):
        ''' Guadar la información de una vacante. '''
        title = self.entryTitle.get()
        title = title.strip()
        company = self.entryCompany.get()
        company = company.strip()
        location = self.entryLocation.get()
        location = location.strip()
        min_salary = self.entryMinSalary.get()
        min_salary = min_salary.strip()
        max_salary = self.entryMaxSalary.get()
        max_salary = max_salary.strip()
        description = self.textDescription.get('1.0', tk.END)
        description = description.strip()
        requirements = self.textRequirements.get('1.0', tk.END)
        requirements = requirements.strip()

        # validar puesto
        if title == '':
            notifyAlert('El puesto es requerido', self.entryTitle)
            return

        # validar empresa
        if company == '':
            notifyAlert('La empresa es requerida', self.entryCompany)
            return

        # validar locacion
        if location == '':
            notifyAlert('La locación es requerida', self.entryLocation)
            return

        # validar salario mínimo
        if min_salary != '' and re.match(r'^[\-\+]?\d+(\.\d*)?$', min_salary) is None:
            notifyAlert('El salario mínimo debe ser un valor numérico', self.entryMinSalary)
            return

        # validar salario máximo
        if max_salary != '' and re.match(r'^[\-\+]?\d+(\.\d*)?$', max_salary) is None:
            notifyAlert('El salario máximo debe ser un valor numérico', self.entryMaxSalary)
            return

        max_salary = None if max_salary == '' else float(max_salary)
        min_salary = None if min_salary == '' else float(min_salary)
        newVacancy = Vacancy(company, description, location, max_salary, min_salary, requirements, title)
        currentVacancy = findVacancy(newVacancy)

        if self.vacancy is None:
            notExists = currentVacancy is None
            if notExists:
                insertVacancy(newVacancy)
        else:
            notExists = currentVacancy is None or currentVacancy is self.vacancy
            if notExists:
                self.vacancy.company = company
                self.vacancy.description = description
                self.vacancy.location = location
                self.vacancy.max_salary = max_salary
                self.vacancy.min_salary = min_salary
                self.vacancy.requirements = requirements
                self.vacancy.title = title

        if notExists:
            message = 'La vacante {0} se ha guardado correctamente.'.format(newVacancy)
            notifySuccess(message)
        else:
            message = 'La vacante {0} ya existe.'.format(newVacancy)
            notifyAlert(message)
        self.close()

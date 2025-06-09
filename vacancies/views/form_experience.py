import re
import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional
from vacancies.entities.applicant import Applicant
from vacancies.entities.experience import Experience
from vacancies.utils import appName, createIcon, notifyAlert, notifySuccess

class FormExperience(tk.Toplevel):

    def __init__(self, parentModal: tk.Toplevel, callback: Callable[[], None]):
        super().__init__(parentModal)
        self.applicant = Applicant()
        self.callback = callback
        self.experience = Experience()

        self.title(appName('Experiencia'))
        self.geometry('400x200')
        self.state('withdrawn')
        self.protocol('WM_DELETE_WINDOW', self.close)

        # configure the grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        # type
        self.iconType = createIcon('suitcase')
        self.labelType = ttk.Label(self, text='Tipo de experiencia:', image=self.iconType, compound=tk.LEFT)
        self.labelType.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
        options = [
            'Selecciona una opción...',
        ]
        self.comboType = ttk.Combobox(self, values=options + Experience.TYPES, state='readonly')
        self.comboType.grid(column=1, row=0, sticky=tk.EW, padx=5, pady=5)

        # title
        self.iconTitle = createIcon('graduation-cap')
        self.labelTitle = ttk.Label(self, text='Puesto o estudio: *', image=self.iconTitle, compound=tk.LEFT)
        self.labelTitle.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
        self.entryTitle = ttk.Entry(self)
        self.entryTitle.grid(column=1, row=1, sticky=tk.EW, padx=5, pady=5)

        # institution
        self.iconInstitution = createIcon('industry')
        self.labelInstitution = ttk.Label(self, text='Empresa o institución:', image=self.iconInstitution, compound=tk.LEFT)
        self.labelInstitution.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)
        self.entryInstitution = ttk.Entry(self)
        self.entryInstitution.grid(column=1, row=2, sticky=tk.EW, padx=5, pady=5)

        # starting year
        self.iconStartingYear = createIcon('calendar')
        self.labelStartingYear = ttk.Label(self, text='Año de inicio:', image=self.iconStartingYear, compound=tk.LEFT)
        self.labelStartingYear.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)
        self.entryStartingYear = ttk.Entry(self)
        self.entryStartingYear.grid(column=1, row=3, sticky=tk.EW, padx=5, pady=5)

        # ending year
        self.iconEndingYear = createIcon('calendar')
        self.labelEndingYear = ttk.Label(self, text='Año final:', image=self.iconEndingYear, compound=tk.LEFT)
        self.labelEndingYear.grid(column=0, row=4, sticky=tk.W, padx=5, pady=5)
        self.entryEndingYear = ttk.Entry(self)
        self.entryEndingYear.grid(column=1, row=4, sticky=tk.EW, padx=5, pady=5)

        # buttons frame
        self.frameButtons = tk.Frame(self)
        self.frameButtons.grid(row=5, column=0, columnspan=2, sticky=tk.E, pady=10)
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

    # Abrir la ventana
    def open(self, applicant:Applicant, experience:Optional[Experience] = None):
        self.applicant = applicant
        self.experience = experience
        self.comboType.current(0)
        self.entryTitle.delete(0, tk.END)
        self.entryInstitution.delete(0, tk.END)
        self.entryStartingYear.delete(0, tk.END)
        self.entryEndingYear.delete(0, tk.END)

        if experience is not None:
            self.comboType.current(experience.type + 1)
            self.entryTitle.insert(0, experience.title)
            self.entryInstitution.insert(0, experience.institution)
            self.entryStartingYear.insert(0, '' if experience.starting_year is None else repr(experience.starting_year))
            self.entryEndingYear.insert(0, '' if experience.ending_year is None else repr(experience.ending_year))

        self.iconify()

    # Cerrar la ventana
    def close(self):
        self.withdraw()
        self.callback()

    # Guadar la información de experiencia
    def store(self):
        type = self.comboType.current() - 1
        title = self.entryTitle.get()
        title = title.strip()
        institution = self.entryInstitution.get()
        institution = institution.strip()
        starting_year = self.entryStartingYear.get()
        starting_year = starting_year.strip()
        ending_year = self.entryEndingYear.get()
        ending_year = ending_year.strip()

        # validar tipo
        if type < 0:
            notifyAlert('Selecciona un tipo de experencia', self.comboType)
            return

        # validar puesto o estudio
        if title == '':
            notifyAlert('El puesto o estudio es requerido', self.entryTitle)
            return

        # validar empresa o institucion
        if institution == '':
            notifyAlert('La empresa o institución es requerida', self.entryInstitution)
            return

        # validar año inicial
        if starting_year != '' and re.match(r'^(19|20)\d\d?$', starting_year) is None:
            notifyAlert('El año inicial es incorrecto', self.entryStartingYear)
            return

        # validar año final
        if ending_year != '' and re.match(r'^(19|20)\d\d?$', ending_year) is None:
            notifyAlert('El año final es incorrecto', self.entryEndingYear)
            return

        ending_year = None if ending_year == '' else int(ending_year)
        starting_year = None if starting_year == '' else int(starting_year)
        newExperience = Experience(ending_year, institution, starting_year, title, type)
        hash = newExperience.hash()
        currentExperience = self.applicant.experience.get(hash)

        if self.experience is None:
            notExists = currentExperience is None
            if notExists:
                self.applicant.experience.set(hash, newExperience)
        else:
            notExists = currentExperience is None or currentExperience is self.experience
            if notExists:
                self.experience.ending_year = ending_year
                self.experience.institution = institution
                self.experience.starting_year = starting_year
                self.experience.title = title
                self.experience.type = type

        if notExists:
            message = 'La experiencia {0} se ha guardado correctamente.'.format(newExperience)
            notifySuccess(message)
        else:
            message = 'La experiencia {0} ya existe.'.format(newExperience)
            notifyAlert(message)
        self.close()

import tkinter as tk
from tkinter import ttk
from tkfontawesome import icon_to_image
from vacancies.utils import appName, notifyAlert

class FormExperience(tk.Toplevel):

    def __init__(self, parentModal):
        super().__init__(parentModal)

        self.title(appName() + ' - Experiencia')
        self.geometry("450x250")
        self.state('withdrawn')
        self.protocol('WM_DELETE_WINDOW', self.onClose)

        # configure the grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        # type
        self.iconType = icon_to_image('suitcase', fill="#4267B2", scale_to_width=16)
        self.labelType = ttk.Label(self, text="Tipo de experiencia:", image=self.iconType, compound=tk.LEFT)
        self.labelType.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
        options = [
            "Selecciona una opción...",
            "Estudio o grado",
            "Puesto anterior",
            "Curso", "Certificación",
        ]
        self.comboType = ttk.Combobox(self, values=options, state='readonly')
        self.comboType.grid(column=1, row=0, sticky=tk.EW, padx=5, pady=5)

        # title
        self.iconTitle = icon_to_image('graduation-cap', fill="#4267B2", scale_to_width=16)
        self.labelTitle = ttk.Label(self, text="Puesto o estudio: *", image=self.iconTitle, compound=tk.LEFT)
        self.labelTitle.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
        self.entryTitle = ttk.Entry(self)
        self.entryTitle.grid(column=1, row=1, sticky=tk.EW, padx=5, pady=5)

        # institution
        self.iconInstitution = icon_to_image('industry', fill="#4267B2", scale_to_width=16)
        self.labelInstitution = ttk.Label(self, text="Empresa o institución:", image=self.iconInstitution, compound=tk.LEFT)
        self.labelInstitution.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)
        self.entryInstitution = ttk.Entry(self)
        self.entryInstitution.grid(column=1, row=2, sticky=tk.EW, padx=5, pady=5)

        # starting year
        self.iconStartingYear = icon_to_image('calendar', fill="#4267B2", scale_to_width=16)
        self.labelStartingYear = ttk.Label(self, text="Año de inicio:", image=self.iconStartingYear, compound=tk.LEFT)
        self.labelStartingYear.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)
        self.entryStartingYear = ttk.Entry(self)
        self.entryStartingYear.grid(column=1, row=3, sticky=tk.EW, padx=5, pady=5)

        # ending year
        self.iconEndingYear = icon_to_image('calendar', fill="#4267B2", scale_to_width=16)
        self.labelEndingYear = ttk.Label(self, text="Año final:", image=self.iconEndingYear, compound=tk.LEFT)
        self.labelEndingYear.grid(column=0, row=4, sticky=tk.W, padx=5, pady=5)
        self.entryEndingYear = ttk.Entry(self)
        self.entryEndingYear.grid(column=1, row=4, sticky=tk.EW, padx=5, pady=5)

        # applicant
        self.iconApplicant = icon_to_image('user-tie', fill="#4267B2", scale_to_width=16)
        self.labelApplicant = ttk.Label(self, text="Candidato: *", image=self.iconApplicant, compound=tk.LEFT)
        self.labelApplicant.grid(column=0, row=5, sticky=tk.W, padx=5, pady=5)
        options = [
            "Selecciona una opción..."
        ]
        self.comboApplicant = ttk.Combobox(self, values=options, state='readonly')
        self.comboApplicant.grid(column=1, row=5, sticky=tk.EW, padx=5, pady=5)

        # buttons frame
        self.frameButtons = tk.Frame(self)
        self.frameButtons.grid(row=6, column=0, columnspan=2, sticky=tk.E, pady=10)
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
        self.comboType.current(0)
        self.entryTitle.delete(0, tk.END)
        self.entryInstitution.delete(0, tk.END)
        self.entryStartingYear.delete(0, tk.END)
        self.entryEndingYear.delete(0, tk.END)
        self.comboApplicant.current(0)
        self.iconify()

        self.callbackOnStore = callbackOnStore

    # Guadar la información de experiencia
    def save(self):
        type = self.comboType.current()
        title = self.entryTitle.get()
        title = title.strip()
        institution = self.entryInstitution.get()
        institution = institution.strip()
        starting_year = self.entryStartingYear.get()
        starting_year = starting_year.strip()
        ending_year = self.entryEndingYear.get()
        ending_year = ending_year.strip()
        applicant = self.comboApplicant.current()

        # validar puesto o estudio
        if title == '':
            notifyAlert('El puesto o estudio es requerido', self.entryTitle)
            return

        # validar candidato
        if applicant == 0:
            notifyAlert('El puesto o estudio es requerido', self.comboApplicant)
            return

        print('ok')
        # if checkIfExists:
        #     notifyAlert('exists')
        #     return
        #self.callbackOnStore()

    # Cerrar la ventana
    def close(self):
        self.withdraw()

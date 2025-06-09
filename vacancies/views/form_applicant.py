import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional
from vacancies.entities.applicant import Applicant
from vacancies.structures.app import findApplicant, insertApplicant
from vacancies.utils import appName, createIcon, notifyAlert, notifySuccess

class FormApplicant(tk.Toplevel):

    def __init__(self, parentModal: tk.Toplevel, callback: Callable[[], None]):
        super().__init__(parentModal)
        self.applicant = Applicant()
        self.callback = callback

        self.title(appName('Candidatos'))
        self.geometry('780x270')
        self.state('withdrawn')
        self.protocol('WM_DELETE_WINDOW', self.close)

        # configure the grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        # first name
        self.iconFirstName = createIcon('id-badge')
        self.labelFirstName = ttk.Label(self, text='Nombres: *', image=self.iconFirstName, compound=tk.LEFT)
        self.labelFirstName.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
        self.entryFirstName = ttk.Entry(self)
        self.entryFirstName.grid(column=1, row=0, sticky=tk.EW, padx=5, pady=5)

        # last name
        self.iconLastName = createIcon('id-badge')
        self.labelLastName = ttk.Label(self, text='Apellidos: *', image=self.iconLastName, compound=tk.LEFT)
        self.labelLastName.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
        self.entryLastName = ttk.Entry(self)
        self.entryLastName.grid(column=1, row=1, sticky=tk.EW, padx=5, pady=5)

        # email
        self.iconEmail = createIcon('at')
        self.labelEmail = ttk.Label(self, text='E-mail:', image=self.iconEmail, compound=tk.LEFT)
        self.labelEmail.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)
        self.entryEmail = ttk.Entry(self)
        self.entryEmail.grid(column=1, row=2, sticky=tk.EW, padx=5, pady=5)

        # phone
        self.iconPhone = createIcon('phone')
        self.labelPhone = ttk.Label(self, text='Teléfono:', image=self.iconPhone, compound=tk.LEFT)
        self.labelPhone.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)
        self.entryPhone = ttk.Entry(self)
        self.entryPhone.grid(column=1, row=3, sticky=tk.EW, padx=5, pady=5)

        # resume
        self.iconResume = createIcon('certificate')
        self.labelResume = ttk.Label(self, text='Currículum:', image=self.iconResume, compound=tk.LEFT)
        self.labelResume.grid(column=0, row=4, sticky=tk.W, padx=5, pady=5)
        self.textResume = tk.Text(self, height=4, width=80)
        self.textResume.grid(column=1, row=4, sticky=tk.EW, padx=5, pady=5)

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
    def open(self, applicant:Optional[Applicant] = None):
        self.applicant = applicant
        self.entryFirstName.delete(0, tk.END)
        self.entryLastName.delete(0, tk.END)
        self.entryEmail.delete(0, tk.END)
        self.entryPhone.delete(0, tk.END)
        self.textResume.delete('1.0', tk.END)

        if applicant is not None:
            self.entryFirstName.insert(0, applicant.first_name)
            self.entryLastName.insert(0, applicant.last_name)
            self.entryEmail.insert(0, applicant.email)
            self.entryPhone.insert(0, applicant.phone)
            self.textResume.insert('1.0', applicant.resume)

        self.iconify()

    # Cerrar la ventana
    def close(self):
        self.withdraw()
        self.callback()

    # Guadar la información de una candidato
    def store(self):
        first_name = self.entryFirstName.get()
        first_name = first_name.strip()
        last_name = self.entryLastName.get()
        last_name = last_name.strip()
        email = self.entryEmail.get()
        email = email.strip()
        phone = self.entryPhone.get()
        phone = phone.strip()
        resume = self.textResume.get('1.0', tk.END)
        resume = resume.strip()

        # validar nombres
        if first_name == '':
            notifyAlert('El nombre es requerido', self.entryFirstName)
            return

        # validar nombres
        if last_name == '':
            notifyAlert('Los apellidos son requeridos', self.entryLastName)
            return

        newApplicant = Applicant(email, first_name, last_name, phone, resume)
        currentApplicant = findApplicant(newApplicant)

        if self.applicant is None:
            notExists = currentApplicant is None
            if notExists:
                insertApplicant(newApplicant)
        else:
            notExists = currentApplicant is None or currentApplicant is self.applicant
            if notExists:
                self.applicant.email = email
                self.applicant.first_name = first_name
                self.applicant.last_name = last_name
                self.applicant.phone = phone
                self.applicant.resume = resume

        self.close()
        if notExists:
            message = 'El candidato {0} se ha guardado correctamente.'.format(newApplicant)
            notifySuccess(message)
        else:
            message = 'El candidato {0} ya existe.'.format(newApplicant)
            notifyAlert(message)
        self.callback()

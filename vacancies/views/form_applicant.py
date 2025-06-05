import tkinter as tk
from tkinter import ttk
from tkfontawesome import icon_to_image
from vacancies.entities.applicant import Applicant
from vacancies.structures.app import insertApplicant
from vacancies.utils import appName, notifyAlert, notifySuccess

class FormApplicant(tk.Toplevel):

    def __init__(self, parentModal):
        super().__init__(parentModal)

        self.title(appName() + ' - Candidatos')
        self.geometry("780x270")
        self.state('withdrawn')
        self.protocol('WM_DELETE_WINDOW', self.onClose)

        # configure the grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        # first name
        self.iconFirstName = icon_to_image('id-badge', fill="#4267B2", scale_to_width=16)
        self.labelFirstName = ttk.Label(self, text="Nombres: *", image=self.iconFirstName, compound=tk.LEFT)
        self.labelFirstName.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
        self.entryFirstName = ttk.Entry(self)
        self.entryFirstName.grid(column=1, row=0, sticky=tk.EW, padx=5, pady=5)

        # last name
        self.iconLastName = icon_to_image('id-badge', fill="#4267B2", scale_to_width=16)
        self.labelLastName = ttk.Label(self, text="Apellidos: *", image=self.iconLastName, compound=tk.LEFT)
        self.labelLastName.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
        self.entryLastName = ttk.Entry(self)
        self.entryLastName.grid(column=1, row=1, sticky=tk.EW, padx=5, pady=5)

        # email
        self.iconEmail = icon_to_image('at', fill="#4267B2", scale_to_width=16)
        self.labelEmail = ttk.Label(self, text="E-mail:", image=self.iconEmail, compound=tk.LEFT)
        self.labelEmail.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)
        self.entryEmail = ttk.Entry(self)
        self.entryEmail.grid(column=1, row=2, sticky=tk.EW, padx=5, pady=5)

        # phone
        self.iconPhone = icon_to_image('phone', fill="#4267B2", scale_to_width=16)
        self.labelPhone = ttk.Label(self, text="Teléfono:", image=self.iconPhone, compound=tk.LEFT)
        self.labelPhone.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)
        self.entryPhone = ttk.Entry(self)
        self.entryPhone.grid(column=1, row=3, sticky=tk.EW, padx=5, pady=5)

        # resume
        self.iconResume = icon_to_image('certificate', fill="#4267B2", scale_to_width=16)
        self.labelResume = ttk.Label(self, text="Currículum:", image=self.iconResume, compound=tk.LEFT)
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
        self.entryFirstName.delete(0, tk.END)
        self.entryLastName.delete(0, tk.END)
        self.entryEmail.delete(0, tk.END)
        self.entryPhone.delete(0, tk.END)
        self.textResume.delete('1.0', tk.END)
        self.iconify()

        self.callbackOnStore = callbackOnStore

    # Guadar la información de una vacante
    def save(self):
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

        print('ok')
        # if checkIfExists:
        #     notifyAlert('exists')
        #     return

        applicant = Applicant(email, first_name, last_name, phone, resume)
        insertApplicant(applicant)
        notifySuccess('El candidato se ha agregado correctamente.')
        self.close()

    # Cerrar la ventana
    def close(self):
        self.withdraw()

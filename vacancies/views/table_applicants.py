import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from typing import Any, Optional
from vacancies.entities.applicant import Applicant
from vacancies.structures.app import findApplicant, forEachApplicant, removeApplicant, sortApplicants
from vacancies.utils import appName, createIcon, notifySuccess
from vacancies.views.form_applicant import FormApplicant
from vacancies.views.table_experience import TableExperience

class TableApplicants(tk.Toplevel):

    def __init__(self, parentModal: tk.Tk):
        super().__init__(parentModal)
        self.modalCreate = FormApplicant(self, self.open)
        self.modalExperience = TableExperience(self, self.open)

        self.title(appName('Candidatos'))
        self.geometry('800x500')
        self.state('withdrawn')
        self.protocol('WM_DELETE_WINDOW', self.close)
        self.resizable(True, True)

        # configure the grid
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=11)
        self.columnconfigure(0, weight=1)

        # buttons frame
        self.frameButtons = tk.Frame(self)
        self.frameButtons.grid(row=0, column=0, sticky=tk.E, pady=10)
        self.frameButtons.rowconfigure(0, weight=1)
        self.frameButtons.rowconfigure(1, weight=1)
        self.frameButtons.rowconfigure(2, weight=1)
        self.frameButtons.rowconfigure(3, weight=1)
        self.frameButtons.columnconfigure(0, weight=1)

        # button delete
        self.iconDestroy = createIcon('trash')
        self.buttonDestroy = ttk.Button(self.frameButtons, text='Eliminar', image=self.iconDestroy, compound=tk.LEFT, command=lambda: self.destroyApplicant())
        self.buttonDestroy.grid(column=0, row=0, padx=5)

        # button experience
        self.iconApplicants = createIcon('user-tie')
        self.buttonExperience = ttk.Button(self.frameButtons, text='Experiencia', image=self.iconApplicants, compound=tk.LEFT, command=lambda: self.showExperience())
        self.buttonExperience.grid(column=1, row=0, padx=5)

        # button edit
        self.iconUpdate = createIcon('pen')
        self.buttonUpdate = ttk.Button(self.frameButtons, text='Editar', image=self.iconUpdate, compound=tk.LEFT, command=lambda: self.updateApplicant())
        self.buttonUpdate.grid(column=2, row=0, padx=5)

        # button create
        self.iconCreate = createIcon('square-plus')
        self.buttonCreate = ttk.Button(self.frameButtons, text='Nuevo', image=self.iconCreate, compound=tk.LEFT, command=lambda: self.createApplicant())
        self.buttonCreate.grid(column=3, row=0, padx=5)

        # Create a Treeview widget
        self.treeview = ttk.Treeview(self)

        # Define the columns
        self.treeview['columns'] = ('Nombres', 'Apellidos', 'Correo', 'Teléfono')

        # Format the columns
        self.treeview.column('#0', width=0, stretch=tk.NO)
        self.treeview.column('Nombres', anchor=tk.W)
        self.treeview.column('Apellidos', anchor=tk.W)
        self.treeview.column('Correo', anchor=tk.W)
        self.treeview.column('Teléfono', anchor=tk.W)

        # Create the headings
        self.iconSort = createIcon('arrow-down-a-z')
        self.treeview.heading('#0', text='', anchor=tk.W)
        self.treeview.heading(
            'Nombres',
            text='Nombres',
            anchor=tk.W,
            image=self.iconSort,
            command=self.sortByFirstName
        )
        self.treeview.heading(
            'Apellidos',
            text='Apellidos',
            anchor=tk.W,
            image=self.iconSort,
            command=self.sortByLastName
        )
        self.treeview.heading(
            'Correo',
            text='Correo',
            anchor=tk.W,
            image=self.iconSort,
            command=self.sortByEmail
        )
        self.treeview.heading(
            'Teléfono',
            text='Teléfono',
            anchor=tk.W,
            image=self.iconSort,
            command=self.sortByPhone
        )

        # Configure alternating row colors
        self.treeview.tag_configure('oddrow', background='#E8E8E8')
        self.treeview.tag_configure('evenrow', background='#FFFFFF')

        # Pack the treeview
        self.treeview.grid(row=1, column=0, sticky=tk.NSEW, pady=10)
        self.treeview.bind('<<TreeviewSelect>>', self.onSelect)

    # Agregar un candidato a la tabla
    def insertApplicant(self, applicant: Applicant, args: Any):
        i = args['i']
        values = [applicant.first_name, applicant.last_name, applicant.email, applicant.phone]
        tag = 'evenrow' if i % 2 == 0 else 'oddrow'
        self.treeview.insert(parent='', index=i, iid=i, values=values, tags=(tag,))
        args['i'] += 1

    # Recargar la tabla
    def reload(self):
        # clear the treeview
        for children in self.treeview.get_children():
            self.treeview.delete(children)
        self.update()

        # fill the treeview
        args = {'i': 0}
        forEachApplicant(self.insertApplicant, args)

        # disable buttons destroy, experience and update
        self.buttonExperience.config(state=tk.DISABLED)
        self.buttonDestroy.config(state=tk.DISABLED)
        self.buttonUpdate.config(state=tk.DISABLED)

    # Abrir la ventana
    def open(self):
        self.reload()
        self.iconify()

    # Cerrar la ventana
    def close(self):
        self.withdraw()

    # Evento al seleccionar un candidato de la tabla
    def onSelect(self, event):
        selection = self.treeview.selection()
        state = tk.NORMAL if len(selection) == 1 else tk.DISABLED
        self.buttonExperience.config(state=state)
        self.buttonDestroy.config(state=state)
        self.buttonUpdate.config(state=state)

    # Retorna el candidato seleccionada en la tabla
    def selectedApplicant(self) -> Optional[Applicant]:
        selection = self.treeview.selection()

        if len(selection) == 0:
            return None

        item = self.treeview.item(selection[0])
        values = item['values']
        applicant = Applicant(first_name=values[0], last_name=values[1])

        return findApplicant(applicant)

    def createApplicant(self):
        self.close()
        self.modalCreate.open()

    def destroyApplicant(self):
        applicant = self.selectedApplicant()

        if applicant is None:
            return

        title = appName()
        message = '¿Quieres eliminar al candidato {0}?'.format(applicant)
        isOk = messagebox.askokcancel(title=title, message=message, icon=messagebox.QUESTION, parent=self)

        if not isOk:
            return

        removeApplicant(applicant)
        message = 'La cantidato {0} se ha eliminado correctamente.'.format(applicant)
        notifySuccess(message)
        self.reload()

    def showExperience(self):
        applicant = self.selectedApplicant()

        if applicant is None:
            return

        self.close()
        self.modalExperience.open(applicant)

    def updateApplicant(self):
        applicant = self.selectedApplicant()

        if applicant is None:
            return

        self.close()
        self.modalCreate.open(applicant)

    def sortByEmail(self):
        sortApplicants('email')
        self.reload()

    def sortByFirstName(self):
        sortApplicants('first_name')
        self.reload()

    def sortByLastName(self):
        sortApplicants('last_name')
        self.reload()

    def sortByPhone(self):
        sortApplicants('phone')
        self.reload()

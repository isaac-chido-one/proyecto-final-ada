import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from typing import Any, Callable, Optional
from vacancies.entities.applicant import Applicant
from vacancies.structures.app import findApplicant, forEachApplicant, removeApplicant, sortApplicants
from vacancies.utils import appName, createIcon, notifySuccess
from vacancies.views.form_applicant import FormApplicant
from vacancies.views.table_experience import TableExperience

class TableApplicants(tk.Toplevel):
    ''' Ventana para el CRUD de candidatos. '''

    def __init__(self, parentModal: tk.Tk, callback: Callable[[], None]):
        ''' Agrgega los widgets necesarios a la ventana. '''
        super().__init__(parentModal)
        self.callback = callback
        self.modalCreate = FormApplicant(self, self.open)
        self.modalExperience = TableExperience(self, self.open)

        self.title(appName('Candidatos'))
        self.geometry('800x500')
        self.state('withdrawn')
        self.protocol('WM_DELETE_WINDOW', self.finalize)
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
        self.iconApplicants = createIcon('graduation-cap')
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

    def insertApplicant(self, applicant: Applicant, args: Any):
        ''' Agregar un candidato a la tabla '''
        i = args['i']
        values = [applicant.first_name, applicant.last_name, applicant.email, applicant.phone]
        tag = 'evenrow' if i % 2 == 0 else 'oddrow'
        self.treeview.insert(parent='', index=i, iid=i, values=values, tags=(tag,))
        args['i'] += 1

    def reload(self):
        ''' Recargar la tabla '''

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

    def open(self):
        ''' Abrir la ventanta y recargar la tabla '''
        state = self.state()
        self.reload()

        if state == 'iconic':
            self.deiconify()
        else:
            self.iconify()

    def close(self):
        ''' Cerrar la ventana '''
        self.withdraw()

    def onSelect(self, event):
        ''' Evento al seleccionar un candidato de la tabla '''
        selection = self.treeview.selection()
        state = tk.NORMAL if len(selection) == 1 else tk.DISABLED
        self.buttonExperience.config(state=state)
        self.buttonDestroy.config(state=state)
        self.buttonUpdate.config(state=state)

    def selectedApplicant(self) -> Optional[Applicant]:
        ''' Retorna el candidato seleccionado en la tabla '''
        selection = self.treeview.selection()

        if len(selection) == 0:
            return None

        item = self.treeview.item(selection[0])
        values = item['values']
        applicant = Applicant(first_name=values[0], last_name=values[1])

        return findApplicant(applicant)

    def createApplicant(self):
        ''' Abre la ventana para crear un nuevo candidato. '''
        self.close()
        self.modalCreate.open()

    def destroyApplicant(self):
        ''' Elimina el candidato seleccionado en la tabla. '''
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
        ''' Abre la tabla de la experiencia del candidato. '''
        applicant = self.selectedApplicant()

        if applicant is None:
            return

        self.close()
        self.modalExperience.open(applicant)

    def updateApplicant(self):
        ''' Abre la ventana para editar el candidato seleccionado. '''
        applicant = self.selectedApplicant()

        if applicant is None:
            return

        self.close()
        self.modalCreate.open(applicant)

    def sortByEmail(self):
        ''' Ordena la tabla de candidatos por correo de menor a mayor. '''
        sortApplicants('email')
        self.reload()

    def sortByFirstName(self):
        ''' Ordena la tabla de candidatos por nombres de menor a mayor. '''
        sortApplicants('first_name')
        self.reload()

    def sortByLastName(self):
        ''' Ordena la tabla de candidatos por apellidos de menor a mayor. '''
        sortApplicants('last_name')
        self.reload()

    def sortByPhone(self):
        ''' Ordena la tabla de candidatos por teléfono de menor a mayor. '''
        sortApplicants('phone')
        self.reload()

    def finalize(self):
        ''' Cierra la ventana y regresa al menú '''
        self.close()
        self.callback()

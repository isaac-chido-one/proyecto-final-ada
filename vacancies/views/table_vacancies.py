import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from typing import Any, Optional
from vacancies.entities.vacancy import Vacancy
from vacancies.structures.app import forEachVacancy, findVacancy, removeVacancy, sortVacancies
from vacancies.utils import appName, createIcon, notifySuccess
from vacancies.views.form_vacancy import FormVacancy

class TableVacancies(tk.Toplevel):

    def __init__(self, parentModal: tk.Tk):
        super().__init__(parentModal)
        self.modal = FormVacancy(parentModal, self.onStore)

        self.title(appName('Vacantes'))
        self.geometry('700x500')
        self.state('withdrawn')
        self.protocol('WM_DELETE_WINDOW', self.onClose)
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
        self.buttonDestroy = ttk.Button(self.frameButtons, text='Eliminar', image=self.iconDestroy, compound=tk.LEFT, command=lambda: self.destroyVacancy())
        self.buttonDestroy.grid(column=0, row=0, padx=5)

        # button applicants
        self.iconApplicants = createIcon('user-tie')
        self.buttonApplicants = ttk.Button(self.frameButtons, text='Candidatos', image=self.iconApplicants, compound=tk.LEFT, command=lambda: self.showApplicants())
        self.buttonApplicants.grid(column=1, row=0, padx=5)

        # button edit
        self.iconUpdate = createIcon('pen')
        self.buttonUpdate = ttk.Button(self.frameButtons, text='Editar', image=self.iconUpdate, compound=tk.LEFT, command=lambda: self.updateVacancy())
        self.buttonUpdate.grid(column=2, row=0, padx=5)

        # button new
        self.iconCreate = createIcon('square-plus')
        self.buttonCreate = ttk.Button(self.frameButtons, text='Nuevo', image=self.iconCreate, compound=tk.LEFT, command=lambda: self.createVacancy())
        self.buttonCreate.grid(column=3, row=0, padx=5)

        # Create a Treeview widget
        self.treeview = ttk.Treeview(self)

        # Define the columns
        self.treeview['columns'] = ('Puesto', 'Empresa', 'Locación')

        # Format the columns
        self.treeview.column('#0', width=0, stretch=tk.NO)
        self.treeview.column('Puesto', anchor=tk.W)
        self.treeview.column('Empresa', anchor=tk.W)
        self.treeview.column('Locación', anchor=tk.W)

        # Create the headings
        self.iconSort = createIcon('arrow-down-a-z')
        self.treeview.heading('#0', text='', anchor=tk.W)
        self.treeview.heading(
            'Puesto',
            text='Puesto',
            anchor=tk.W,
            image=self.iconSort,
            command=self.sortByTitle
        )
        self.treeview.heading(
            'Empresa',
            text='Empresa',
            anchor=tk.W,
            image=self.iconSort,
            command=self.sortByCompany
        )
        self.treeview.heading(
            'Locación',
            text='Locación',
            anchor=tk.W,
            image=self.iconSort,
            command=self.sortByLocation
        )

        # Configure alternating row colors
        self.treeview.tag_configure('oddrow', background='#E8E8E8')
        self.treeview.tag_configure('evenrow', background='#FFFFFF')

        # Pack the treeview
        self.treeview.grid(row=1, column=0, sticky=tk.NSEW, pady=10)
        self.treeview.bind('<<TreeviewSelect>>', self.onSelect)

    # Evento al cerrar la ventana
    def onClose(self):
        self.close()

    # Agregar una vacante a la tabla
    def insertVacancy(self, vacancy: Vacancy, args: Any):
        i = args['i']
        values = [vacancy.title, vacancy.company, vacancy.location]
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
        forEachVacancy(self.insertVacancy, args)

        # disable buttons destroy and update
        self.buttonApplicants.config(state=tk.DISABLED)
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
        self.buttonApplicants.config(state=state)
        self.buttonDestroy.config(state=state)
        self.buttonUpdate.config(state=state)

    def onStore(self):
        self.reload()
        self.iconify()

    # Retorna la vacante seleccionada en la tabla
    def selectedVacancy(self) -> Optional[Vacancy]:
        selection = self.treeview.selection()
        if len(selection) == 0:
            return None

        item = self.treeview.item(selection[0])
        values = item['values']
        vacancy = Vacancy(title=values[0], company=values[1], location=values[2])

        return findVacancy(vacancy)

    def createVacancy(self):
        self.close()
        self.modal.open()

    def destroyVacancy(self):
        vacancy = self.selectedVacancy()

        if vacancy is None:
            return

        title = appName()
        message = '¿Quieres eliminar la vacante {0}?'.format(vacancy)
        isOk = messagebox.askokcancel(title=title, message=message, icon=messagebox.QUESTION, parent=self)

        if not isOk:
            return

        removeVacancy(vacancy)
        message = 'La vacante {0} se ha eliminado correctamente.'.format(vacancy)
        notifySuccess(message)
        self.reload()

    def showApplicants(self):
        vacancy = self.selectedVacancy()

        if vacancy is None:
            return

        print(vacancy)

    def updateVacancy(self):
        vacancy = self.selectedVacancy()

        if vacancy is None:
            return

        self.close()
        self.modal.open(vacancy)

    def sortByCompany(self):
        sortVacancies('company')
        self.reload()

    def sortByLocation(self):
        sortVacancies('location')
        self.reload()

    def sortByTitle(self):
        sortVacancies('title')
        self.reload()

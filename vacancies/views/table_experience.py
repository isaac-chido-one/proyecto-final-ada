import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from typing import Any, Callable, Optional
from vacancies.entities.applicant import Applicant
from vacancies.entities.experience import Experience
from vacancies.utils import appName, createIcon, notifySuccess
from vacancies.views.form_experience import FormExperience

class TableExperience(tk.Toplevel):
	''' Ventana para el CRUD de experiencia por candidato. '''

	def __init__(self, parentModal: tk.Toplevel, callback: Callable[[], None]):
		''' Agrgega los widgets necesarios a la ventana. '''
		super().__init__(parentModal)
		self.callback = callback
		self.modal = FormExperience(parentModal, self.onUpdate)
		self.applicant = Applicant()

		self.title(appName('Experiencia por empleado'))
		self.geometry('1000x500')
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
		self.frameButtons.columnconfigure(0, weight=1)

		# button destroy
		self.iconDestroy = createIcon('trash')
		self.buttonDestroy = ttk.Button(self.frameButtons, text='Eliminar', image=self.iconDestroy, compound=tk.LEFT, command=lambda: self.destroyExperience())
		self.buttonDestroy.grid(column=0, row=0, padx=5)

		# button edit
		self.iconUpdate = createIcon('pen')
		self.buttonUpdate = ttk.Button(self.frameButtons, text='Editar', image=self.iconUpdate, compound=tk.LEFT, command=lambda: self.updateExperience())
		self.buttonUpdate.grid(column=1, row=0, padx=5)

		# button create
		self.iconCreate = createIcon('square-plus')
		self.buttonCreate = ttk.Button(self.frameButtons, text='Nuevo', image=self.iconCreate, compound=tk.LEFT, command=lambda: self.createExperience())
		self.buttonCreate.grid(column=2, row=0, padx=5)

		# Create a Treeview widget
		self.treeview = ttk.Treeview(self)

		# Define the columns
		self.treeview['columns'] = ('Tipo', 'Puesto-Estudio', 'Empresa-Inst.', 'Año inicial', 'Año final')

		# Format the columns
		self.treeview.column('#0', width=0, stretch=tk.NO)
		self.treeview.column('Tipo', anchor=tk.W)
		self.treeview.column('Puesto-Estudio', anchor=tk.W)
		self.treeview.column('Empresa-Inst.', anchor=tk.W)
		self.treeview.column('Año inicial', anchor=tk.W)
		self.treeview.column('Año final', anchor=tk.W)

		# Create the headings
		self.iconSort = createIcon('arrow-down-a-z')
		self.treeview.heading('#0', text='', anchor=tk.W)
		self.treeview.heading('Tipo', text='Tipo', anchor=tk.W)
		self.treeview.heading(
			'Puesto-Estudio',
			text='Puesto-Estudio',
			anchor=tk.W,
			image=self.iconSort,
			command=self.sortByTitle
		)
		self.treeview.heading(
			'Empresa-Inst.',
			text='Empresa-Inst.',
			anchor=tk.W,
			image=self.iconSort,
			command=self.sortByInstitution
		)
		self.treeview.heading(
			'Año inicial',
			text='Año inicial',
			anchor=tk.W,
			image=self.iconSort,
			command=self.sortByStartingYear
		)
		self.treeview.heading(
			'Año final',
			text='Año final',
			anchor=tk.W,
			image=self.iconSort,
			command=self.sortByEndingYear
		)

		# Configure alternating row colors
		self.treeview.tag_configure('oddrow', background='#E8E8E8')
		self.treeview.tag_configure('evenrow', background='#FFFFFF')

		# Pack the treeview
		self.treeview.grid(row=1, column=0, sticky=tk.NSEW, pady=10)
		self.treeview.bind('<<TreeviewSelect>>', self.onSelect)

	def insertExperience(self, experience: Experience, args: Any):
		''' Agrega un registro de experiencia a la tabla. '''
		i = args['i']
		values = [
			experience.repr_type,
			experience.title,
			experience.institution,
			'' if experience.starting_year is None else repr(experience.starting_year),
			'' if experience.ending_year is None else repr(experience.ending_year),
		]
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
		self.applicant.experience.each(self.insertExperience, args)

		# disable buttons destroy and experience
		self.buttonUpdate.config(state=tk.DISABLED)
		self.buttonDestroy.config(state=tk.DISABLED)

	def open(self, applicant: Applicant):
		''' Abrir la ventanta y recargar la tabla '''
		self.applicant = applicant
		self.onUpdate()

	def close(self):
		''' Cerrar la ventana '''
		self.withdraw()
		self.callback()

	def onSelect(self, event):
		''' Evento al seleccionar un registro de experiencia de la tabla '''
		selection = self.treeview.selection()
		state = tk.NORMAL if len(selection) == 1 else tk.DISABLED
		self.buttonUpdate.config(state=state)
		self.buttonDestroy.config(state=state)

	def onUpdate(self):
		''' Evento al cerrar una ventana hija. '''
		self.reload()
		self.iconify()

	def selectedExperience(self) -> Optional[Experience]:
		''' Retorna la experiencia seleccionada en la tabla '''
		selection = self.treeview.selection()

		if len(selection) == 0:
			return None

		item = self.treeview.item(selection[0])
		values = item['values']
		type = Experience.TYPES.index(values[0])
		title = values[1]
		institution = values[2]
		applicant = Experience(type=type, title=title, institution=institution)
		hash = applicant.hash()

		return self.applicant.experience.get(hash)

	def createExperience(self):
		''' Abre la ventana para crear un nuevo registro de experiencia. '''
		self.withdraw()
		self.modal.open(self.applicant)

	def destroyExperience(self):
		''' Elimina la experiencia seleccionada en la tabla. '''
		experience = self.selectedExperience()

		if experience is None:
			return

		title = appName()
		message = '¿Quieres eliminar la experiencia {0} del candidato {1}?'.format(experience, self.applicant)
		isOk = messagebox.askokcancel(title=title, message=message, icon=messagebox.QUESTION, parent=self)

		if not isOk:
			return

		hash = experience.hash()
		self.applicant.experience.unset(hash)
		message = 'La experiencia {0} se ha eliminado correctamente de la vacante {1}.'.format(experience, self.applicant)
		notifySuccess(message)
		self.reload()

	def updateExperience(self):
		''' Abre la ventana para editar el registro seleccionado de experiencia. '''
		experience = self.selectedExperience()

		if experience is None:
			return

		self.withdraw()
		self.modal.open(self.applicant, experience)

	def sortByTitle(self):
		''' Ordena la tabla de experiencia por puesto o estudio de menor a mayor. '''
		self.applicant.experience.insertSort('title')
		self.reload()

	def sortByInstitution(self):
		''' Ordena la tabla de experiencia por empresa o institución de menor a mayor. '''
		self.applicant.experience.insertSort('institution')
		self.reload()

	def sortByStartingYear(self):
		''' Ordena la tabla de experiencia por año inicial de menor a mayor. '''
		self.applicant.experience.insertSort('starting_year')
		self.reload()

	def sortByEndingYear(self):
		''' Ordena la tabla de experiencia por año final de menor a mayor. '''
		self.applicant.experience.insertSort('ending_year')
		self.reload()

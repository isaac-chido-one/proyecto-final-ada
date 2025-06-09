import tkinter as tk
from tkinter import ttk
from typing import Any, Callable, Optional
from vacancies.entities.applicant import Applicant
from vacancies.entities.vacancy import Vacancy
from vacancies.structures.app import forEachApplicant, findApplicant
from vacancies.utils import appName, appendToArray, createIcon, notifySuccess

class SelectApplicant(tk.Toplevel):

	def __init__(self, parentModal: tk.Toplevel, callback: Callable[[], None]):
		super().__init__(parentModal)
		self.callback = callback
		self.vacancy = Vacancy()

		self.title(appName('Candidatos'))
		self.geometry('700x500')
		self.state('withdrawn')
		self.protocol('WM_DELETE_WINDOW', self.close)
		self.resizable(True, True)

		# configure the grid
		self.rowconfigure(0, weight=11)
		self.rowconfigure(1, weight=1)
		self.columnconfigure(0, weight=1)

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
		self.treeview.heading('#0', text='', anchor=tk.W)
		self.treeview.heading('Nombres', text='Nombres', anchor=tk.W)
		self.treeview.heading('Apellidos', text='Apellidos', anchor=tk.W)
		self.treeview.heading('Correo', text='Correo', anchor=tk.W)
		self.treeview.heading('Teléfono', text='Teléfono', anchor=tk.W)

		# Configure alternating row colors
		self.treeview.tag_configure('oddrow', background='#E8E8E8')
		self.treeview.tag_configure('evenrow', background='#FFFFFF')

		# Pack the treeview
		self.treeview.grid(row=0, column=0, sticky=tk.NSEW, pady=10)
		self.treeview.bind('<<TreeviewSelect>>', self.onSelect)

		# buttons frame
		self.frameButtons = tk.Frame(self)
		self.frameButtons.grid(row=1, column=0, sticky=tk.E, pady=10)
		self.frameButtons.rowconfigure(0, weight=1)
		self.frameButtons.rowconfigure(1, weight=1)
		self.frameButtons.rowconfigure(2, weight=1)
		self.frameButtons.rowconfigure(3, weight=1)
		self.frameButtons.columnconfigure(0, weight=1)

		# button delete
		self.iconCancel = createIcon('xmark')
		self.buttonCancel = ttk.Button(self.frameButtons, text='Cancelar', image=self.iconCancel, compound=tk.LEFT, command=lambda: self.close())
		self.buttonCancel.grid(column=0, row=0, padx=5)

		# button new
		self.iconApply = createIcon('check')
		self.buttonApply = ttk.Button(self.frameButtons, text='Postular', image=self.iconApply, compound=tk.LEFT, command=lambda: self.apply())
		self.buttonApply.grid(column=1, row=0, padx=5)

	def removeApplicant(self, applicant: Applicant, applicants):
		applicants.remove(applicant)

	# Recargar la tabla
	def reload(self):
		# clear the treeview
		for children in self.treeview.get_children():
			self.treeview.delete(children)
		self.update()

		# fill the treeview
		applicants = []
		forEachApplicant(appendToArray, applicants)
		self.vacancy.applicants.each(self.removeApplicant, applicants)
		i = 0

		for applicant in applicants:
			values = [applicant.first_name, applicant.last_name, applicant.email, applicant.phone]
			tag = 'evenrow' if i % 2 == 0 else 'oddrow'
			self.treeview.insert(parent='', index=i, iid=i, values=values, tags=(tag,))
			i += 1

		# disable button apply
		self.buttonApply.config(state=tk.DISABLED)

	# Abrir la ventana
	def open(self, vacancy: Vacancy):
		self.vacancy = vacancy
		self.reload()
		self.iconify()

	# Cerrar la ventana
	def close(self):
		self.withdraw()
		self.callback()

	# Evento al seleccionar un candidato de la tabla
	def onSelect(self, event):
		selection = self.treeview.selection()
		state = tk.NORMAL if len(selection) == 1 else tk.DISABLED
		self.buttonApply.config(state=state)

	def onStore(self):
		self.reload()
		self.iconify()

	# Retorna el candidato seleccionada en la tabla
	def selectedApplicant(self) -> Optional[Applicant]:
		selection = self.treeview.selection()

		if len(selection) == 0:
			return None

		item = self.treeview.item(selection[0])
		values = item['values']
		applicant = Applicant(first_name=values[0], last_name=values[1])

		return findApplicant(applicant)

	def apply(self):
		applicant = self.selectedApplicant()

		if applicant is None:
			return

		self.vacancy.applicants.Apilar(applicant)
		message = 'El cantidato {0} se ha postulado correctamente de la vacante {1}.'.format(applicant, self.vacancy)
		notifySuccess(message)
		self.close()

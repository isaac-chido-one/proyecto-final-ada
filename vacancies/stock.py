import tkinter as tk
from fruit_store.form import Form
from fruit_store.fruits import *
from tkfontawesome import icon_to_image
from tkinter import ttk

class Stock(tk.Toplevel):

    # inicializa la ventana de inventario
    def __init__(self, parentModal):
        super().__init__(parentModal)
        self.modal = None

        self.geometry('800x600')
        self.state('withdrawn')
        self.protocol('WM_DELETE_WINDOW', self.onClose)
        self.title(appName() + ' - Inventario')
        self.resizable(True, True)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # main frame 
        self.frame = tk.Frame(self)
        self.frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=10)
        self.frame.rowconfigure(3, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)

        # search frame
        self.frameSearch = tk.Frame(self.frame)
        self.frameSearch.grid(row=0, column=0, sticky=tk.W)
        self.frameSearch.rowconfigure(0, weight=1)
        self.frameSearch.rowconfigure(1, weight=3)
        self.frameSearch.columnconfigure(0, weight=1)

        # buttons frame
        self.frameButtons = tk.Frame(self.frame)
        self.frameButtons.grid(row=0, column=1, sticky=tk.E)
        self.frameButtons.rowconfigure(0, weight=1)
        self.frameButtons.rowconfigure(1, weight=1)
        self.frameButtons.rowconfigure(2, weight=1)
        self.frameButtons.columnconfigure(0, weight=1)

        # create button
        self.iconCreate = icon_to_image('plus', fill="#4267B2", scale_to_width=16)
        self.buttonCreate = ttk.Button(self.frameButtons, text='Agregar', image=self.iconCreate, compound=tk.LEFT, command=lambda: self.openCreateModal())
        self.buttonCreate.grid(column=0, row=0, padx=5)

        # update button
        self.iconUpdate = icon_to_image('pencil-alt', fill="#4267B2", scale_to_width=16)
        self.buttonUpdate = ttk.Button(self.frameButtons, text='Editar', image=self.iconUpdate, compound=tk.LEFT, command=lambda: self.openUpdateModal())
        self.buttonUpdate.grid(column=1, row=0, padx=5)

        # destroy button
        self.iconDestroy = icon_to_image('minus', fill="#4267B2", scale_to_width=16)
        self.buttonDestroy = ttk.Button(self.frameButtons, text='Eliminar', image=self.iconDestroy, compound=tk.LEFT, command=lambda: self.destroyItem())
        self.buttonDestroy.grid(column=2, row=0, padx=5)

        # table
        style = ttk.Style(self)
        style.configure('STOCK.Treeview', rowheight=35)
        self.treeview = ttk.Treeview(self.frame, columns=('code', 'item', 'cost'), style='STOCK.Treeview')
        self.treeview.heading('#0', text='')
        self.treeview.heading('code', text='Código')
        self.treeview.heading('item', text='Fruta')
        self.treeview.heading('cost', text='Costo')
        self.treeview.column('#0', anchor=tk.CENTER)
        self.treeview.column('code', anchor=tk.CENTER)
        self.treeview.column('cost', anchor=tk.E)
        self.treeview.grid(column=0, row=1, columnspan=2, sticky=tk.NSEW)
        self.treeview.bind('<<TreeviewSelect>>', self.onSelect)
        self.reloadItems()
        self.onSelect(None)

    # Abre el formulario para crear una fruta
    def openCreateModal(self):
        if self.modal is None:
            self.modal = Form(self)
        self.modal.open(None, self.onCreate)

    # Evento al dar click en aceptar del formulario para crear fruta
    def onCreate(self, code, item, cost, image):
        setFruit(code, item, cost, image)
        notifySuccess('Articulo creado correctamente')
        self.reloadItems()

    # Carga la tabla de frutas con información
    def reloadItems(self):
        items = getFruits()
        self.images = {}

        for children in self.treeview.get_children():
            self.treeview.delete(children)
        self.update()

        for code in items:
            self.images[code] = createIcon(code, 32)
            self.treeview.insert(
                "",
                tk.END,
                image=self.images[code],
                values=(code, items[code]['item'], "${0:,.2f}".format(items[code]['cost']))
            )
    
    # Evento al seleccionar una fruta de la tabla
    def onSelect(self, event):
        selection = self.treeview.selection()
        if len(selection) == 1:
            self.buttonDestroy.config(state=tk.NORMAL)
            self.buttonUpdate.config(state=tk.NORMAL)
        else:
            self.buttonDestroy.config(state=tk.DISABLED)
            self.buttonUpdate.config(state=tk.DISABLED)

    # Retorna el código de la fruta seleccionada en la tabla
    def selectedCode(self):
        selection = self.treeview.selection()
        if len(selection) > 0:
            item = self.treeview.item(selection[0])
            if self.modal is None:
                self.modal = Form(self)
            code = item['values'][0]
            return str(code)
        return None

    # Abre el formulario para editar una fruta
    def openUpdateModal(self):
        code = self.selectedCode()
        if not code is None:
            self.modal.open(code, self.onUpdate)

    # Evento al dar click en aceptar del formulario para editar fruta
    def onUpdate(self, code, item, cost, image):
        setFruit(code, item, cost, image)
        notifySuccess('Articulo actualizado correctamente')
        self.reloadItems()

    # Eliminar una fruta
    def destroyItem(self):
        code = self.selectedCode()
        if not code is None and unsetFruit(code):
            notifySuccess('Articulo elimado correctamente')
            self.reloadItems()

    def onClose(self):
        self.withdraw()

import re
import tkinter as tk
from fruit_store.fruits import *
from tkfontawesome import icon_to_image
from tkinter import ttk

class Pos(tk.Toplevel):

    # inicializa la ventana de inventario
    def __init__(self, parentModal):
        super().__init__(parentModal)
        self.shoppingCar = {}

        self.geometry('800x600')
        self.state('withdrawn')
        self.protocol('WM_DELETE_WINDOW', self.onClose)
        self.title(appName() + ' - Punto de venta')
        self.resizable(True, True)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # styling
        self.style = ttk.Style()
        self.style.configure('POS.TLabel', background='white')
        self.style.configure('POS.Treeview', rowheight=70, font=(None, 16))
        self.style.configure('POS.TButton', background='white')

        # frame 
        self.frame = tk.Frame(self)
        self.frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.columnconfigure(0, weight=2)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=2)

        # table
        self.treeview = ttk.Treeview(self.frame, columns=('item'), style='POS.Treeview')
        self.treeview.heading('#0')
        self.treeview.heading('item')
        self.treeview.column('#0', anchor=tk.CENTER, width=70)
        self.treeview.grid(column=0, row=0, rowspan=2, sticky=tk.NSEW, padx=5, pady=5)
        self.treeview.bind('<<TreeviewSelect>>', self.onSelect)

        # Información de la fruta
        self.frameItem = tk.Frame(self.frame, bg='white')
        self.frameItem.grid(row=0, column=1, sticky=tk.N, pady=5)

        self.labelImage = ttk.Label(self.frameItem, style='POS.TLabel', relief=tk.GROOVE)
        self.labelImage.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        label = ttk.Label(self.frameItem, text='Código:', justify=tk.LEFT, style='POS.TLabel')
        label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        label = ttk.Label(self.frameItem, text='Artículo:', justify=tk.LEFT, style='POS.TLabel')
        label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        label = ttk.Label(self.frameItem, text='Costo Kg:', justify=tk.LEFT, style='POS.TLabel')
        label.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        label = ttk.Label(self.frameItem, text='Peso Kg:', justify=tk.LEFT, style='POS.TLabel')
        label.grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        label = ttk.Label(self.frameItem, text='Precio:', justify=tk.LEFT, style='POS.TLabel')
        label.grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)

        self.labelCode = ttk.Label(self.frameItem, justify=tk.RIGHT, style='POS.TLabel', relief=tk.SUNKEN, anchor=tk.E)
        self.labelCode.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)
        self.labelItem = ttk.Label(self.frameItem, justify=tk.RIGHT, style='POS.TLabel', relief=tk.SUNKEN, anchor=tk.E)
        self.labelItem.grid(row=2, column=1, sticky=tk.EW, padx=5, pady=5)
        self.labelCost = ttk.Label(self.frameItem, justify=tk.RIGHT, style='POS.TLabel', relief=tk.SUNKEN, anchor=tk.E)
        self.labelCost.grid(row=3, column=1, sticky=tk.EW, padx=5, pady=5)

        self.varWeight = tk.StringVar()
        self.varWeight.trace_add('write', self.onWeightChange)
        self.entryWeight = ttk.Entry(self.frameItem, textvariable=self.varWeight, justify=tk.RIGHT)
        self.entryWeight.grid(row=4, column=1, sticky=tk.EW, padx=5, pady=5)

        self.labelPrice = ttk.Label(self.frameItem, justify=tk.RIGHT, style='POS.TLabel', relief=tk.SUNKEN, anchor=tk.E)
        self.labelPrice.grid(row=5, column=1, sticky=tk.EW, padx=5, pady=5)

        # button add item
        self.iconAddItem = icon_to_image('angle-double-right', fill="#4267B2", scale_to_width=32)
        self.buttonAddItem = ttk.Button(self.frameItem, text='Comprar', image=self.iconAddItem, compound=tk.RIGHT, style='POS.TButton', command=lambda: self.addItem())
        self.buttonAddItem.grid(row=6, column=0, columnspan=2, sticky=tk.E, padx=5, pady=20)

        # frame carrito de compras
        self.frameShopping = tk.Frame(self.frame)
        self.frameShopping.grid(row=0, column=2, rowspan=2, padx=5, pady=5, sticky=tk.NSEW)

        # listado carrito de compras
        self.scrollbarShopping = ttk.Scrollbar(self.frameShopping, orient=tk.VERTICAL)
        self.listboxShopping = tk.Listbox(self.frameShopping, yscrollcommand=self.scrollbarShopping.set)
        self.listboxShopping.config(font=('TkFixedFont'))
        self.scrollbarShopping.config(command=self.listboxShopping.yview)
        self.scrollbarShopping.pack(side=tk.RIGHT, fill=tk.Y)
        self.listboxShopping.pack(expand=True, fill=tk.BOTH)

        # frame del total
        self.frameTotal = tk.Frame(self.frame, bg='white')
        self.frameTotal.grid(row=1, column=1, padx=5, pady=5, sticky=tk.S)
        self.frameTotal.rowconfigure(0, weight=1)
        self.frameTotal.rowconfigure(1, weight=1)
        self.frameTotal.columnconfigure(0, weight=1)
        self.frameTotal.columnconfigure(1, weight=1)

        label = ttk.Label(self.frameTotal, text='Total:', justify=tk.LEFT, style='POS.TLabel')
        label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

        self.labelTotal = ttk.Label(self.frameTotal, justify=tk.RIGHT, style='POS.TLabel', relief=tk.SUNKEN, anchor=tk.E)
        self.labelTotal.grid(column=1, row=0, sticky=tk.EW, padx=5, pady=5)

        # botón pagar
        self.iconPay = icon_to_image('credit-card', fill="#4267B2", scale_to_width=32)
        self.buttonPay = ttk.Button(self.frameTotal, text='Pagar', image=self.iconPay, compound=tk.RIGHT, style='POS.TButton', command=lambda: self.pay())
        self.buttonPay.grid(column=1, row=1, columnspan=2, sticky=tk.E, padx=5, pady=20)

        self.reloadItems()
        self.onSelect(None)
        self.reloadShoppingCar()

    # Carga la tabla de frutas con información
    def reloadItems(self):
        items = getFruits()
        self.images = {}

        for children in self.treeview.get_children():
            self.treeview.delete(children)
        self.update()

        for code in items:
            self.images[code] = createIcon(code, 64)
            self.treeview.insert(
                "",
                tk.END,
                image=self.images[code],
                values=(' ' + items[code]['item'], code)
            )

    # Retorna el código de la fruta seleccionada en la tabla
    def selectedCode(self):
        selection = self.treeview.selection()
        if len(selection) > 0:
            item = self.treeview.item(selection[0])
            code = item['values'][1]
            return str(code)
        return None

    # Evento al seleccionar una fruta de la tabla
    def onSelect(self, event):
        selection = self.treeview.selection()
        self.entryWeight.config(state=tk.NORMAL)
        self.entryWeight.delete(0, tk.END)
        code = self.selectedCode()
        fruit = None if code is None else findFruit(code)
        self.image = createIcon(code, 128);
        self.labelImage.config(image = self.image)
        self.labelCode.config(text = '---' if fruit is None else code)
        self.labelItem.config(text = '---' if fruit is None else fruit['item'])
        self.labelCost.config(text = '---' if fruit is None else "${0:,.2f}".format(fruit['cost']))
        self.labelPrice.config(text='$0.00')
        self.buttonAddItem.config(state=tk.DISABLED)

        if fruit is None:
            self.entryWeight.config(state=tk.DISABLED)
        else:
            self.entryWeight.focus()

    # evento al editar el peso del artículo
    def onWeightChange(self, var, index, mode):
        weight = self.varWeight.get()
        price = 0
        code = self.selectedCode()

        if not code is None and not re.match(r'^[\-\+]?\d+(\.\d*)?$', weight) is None:
            fruit = findFruit(code)
            price = float(weight) * fruit['cost']
            self.buttonAddItem.config(state=tk.NORMAL)
        else:
            self.buttonAddItem.config(state=tk.DISABLED)
        
        self.labelPrice.config(text = "${0:,.2f}".format(price))

    # Agrgar artículo al carrito de compras
    def addItem(self):
        weight = self.varWeight.get()
        code = self.selectedCode()

        if code is None or re.match(r'^[\-\+]?\d+(\.\d*)?$', weight) is None:
            return

        if code in self.shoppingCar:
            self.shoppingCar[code] += float(weight)
        else:
            self.shoppingCar[code] = float(weight)

        for item in self.treeview.selection():
            self.treeview.selection_remove(item)

        self.reloadShoppingCar()

    # Llenar la información del carrito de compras
    def reloadShoppingCar(self):
        self.listboxShopping.delete(0, tk.END)
        total = 0

        for code in self.shoppingCar:
            fruit = findFruit(code)
            weight = self.shoppingCar[code]
            subtotal = weight * fruit['cost']
            total += subtotal
            self.listboxShopping.insert(tk.END, "{0:<5}{1:>19}".format(code, fruit['item']))
            self.listboxShopping.insert(tk.END, "{0:>8.4f}kg{1:>14}".format(weight, "${0:,.2f}".format(subtotal)))
            self.listboxShopping.insert(tk.END, '------------------------')

        self.labelTotal.config(text = "${0:,.2f}".format(total))

        if total == 0:
            self.buttonPay.config(state=tk.DISABLED)
        else:
            self.buttonPay.config(state=tk.NORMAL)

    # Quitar la información del carrito de compras
    def clearShoppingCar(self):
        self.shoppingCar = {}
        for item in self.treeview.selection():
            self.treeview.selection_remove(item)
        self.reloadShoppingCar()

    # Acción al pagar
    def pay(self):
        self.clearShoppingCar()
        notifySuccess('Compra realizada')

    # Abrir la ventana
    def open(self):
        self.clearShoppingCar()
        self.iconify()

    def onClose(self):
        self.withdraw()

import tkinter as tk
import tksvg
from notifypy import Notify
from tkfontawesome import icon_to_image
from typing import Any, Optional

def appName(sufix:Optional[str] = None) -> str:
    ''' Obtiene el nombre de la aplicación. Para los títulos de las ventanas '''
    name = 'Catálogo de vacantes de empresas'

    if not sufix is None:
        name += ' - ' + sufix

    return name

def appendToArray(element: Any, array):
    ''' Agrega los elementos de una lista ligada a un arreglo. '''
    array.append(element)

def appendDictionaryToArray(element, array):
	''' Agrega los elementos convertidos a diccionario de una lista ligada a un arreglo. '''
	array.append(element.to_dictionary())

def createIcon(awesomeName: str) -> tksvg.SvgImage:
    '''
    Crea íconos a partir de la fuente awesome.

    See:
        https://fontawesome.com/v6/icons?ic=free
    '''
    return icon_to_image(awesomeName, fill='#4267B2', scale_to_width=16)

def notify(title: str, message: str):
    ''' Muestra una notificación en el escritorio. '''
    notification = Notify()
    notification.application_name = appName()
    notification.title = title
    notification.message = message
    notification.send(block=False)

def notifyAlert(message: str, entry:Optional[tk.Entry] = None):
    ''' Muestra una notificación de alerta en el escritorio. '''
    notify('⚠ Alerta', message)

    if not entry is None:
        entry.focus()

def notifySuccess(message: str):
    ''' Muestra una notificación de éxito en el escritorio. '''
    notify('✓ Éxito', message)

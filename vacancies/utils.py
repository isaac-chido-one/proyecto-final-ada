import tkinter as tk
import tksvg
from notifypy import Notify
from tkfontawesome import icon_to_image
from typing import Any, Optional

# Obtiene el nombre de la aplicación
def appName(sufix:Optional[str] = None) -> str:
    name = 'Catálogo de vacantes de empresas'

    if not sufix is None:
        name += ' - ' + sufix

    return name

def appendToArray(element: Any, array):
    array.append(element)

def createIcon(awesomeName: str) -> tksvg.SvgImage:
    return icon_to_image(awesomeName, fill='#4267B2', scale_to_width=16)

# Notificación de éxito
def notify(title: str, message: str):
    notification = Notify()
    notification.application_name = appName()
    notification.title = title
    notification.message = message
    notification.send(block=False)

# Notificación de alerta
def notifyAlert(message: str, entry:Optional[tk.Entry] = None):
    notify('⚠ Alerta', message)

    if not entry is None:
        entry.focus()

# Notificación de éxito
def notifySuccess(message: str):
    notify('✓ Éxito', message)

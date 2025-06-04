import json
import os
import shutil
from notifypy import Notify
from tkfontawesome import icon_to_image

items = {}
source_file = ''

# Obtiene el nombre de la aplicación
def appName() -> str:
    return 'Catálogo de vacantes de empresas'

# Obtiene el directorio del storage
def dirStorage(subdir = '') -> str:
    global source_file
    directory = os.path.dirname(os.path.abspath(source_file)) + os.sep + 'storage'

    if subdir != '':
        directory = directory + os.sep + subdir

    return directory

# Obtiene el directorio del archivo de datos
def dirData() -> str:
    return dirStorage('data')

# Obtiene la ruta del archivo de datos
def fileData() -> str:
    return dirData() + os.sep + 'items.json'

# Carga el listado de frutas
def loadStructures(sourceFile):
    global items
    global source_file
    source_file = sourceFile
    directories = [
        dirStorage(),
        dirData(),
    ]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
    filename = fileData()
    if os.path.exists(filename):
        with open(filename) as json_file:
            items = json.load(json_file)

# Guarda el listado de frutas
def saveData():
    global items
    js = json.dumps(items)
    filename = fileData()
    file = open(filename, 'w')
    file.write(js)
    file.close()

# Notificación de éxito
def notify(title, message):
    notification = Notify()
    notification.application_name = appName()
    notification.title = title
    notification.message = message
    notification.send(block=False)

# Notificación de alerta
def notifyAlert(message, entry = None):
    notify('⚠ Alerta', message)

    if not entry is None:
        entry.focus()

# Notificación de éxito
def notifySuccess(message):
    notify('✓ Éxito', message)

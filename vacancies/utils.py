import json
import os
import shutil
from notify import notification
from PIL import Image, ImageTk
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

# Obtiene el directorio de las imagenes
def dirImages(filename = None) -> str:
    path = dirStorage('images')

    if not filename is None:
        path = path + os.sep + filename

    return path

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
        dirImages(),
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

# Guarda una fruta
def setFruit(code, item, cost, image):
    global items

    # validar imagen
    if not image is None and (not code in items or items[code]['image'] is None or items[code]['image'] != image):
        shutil.copy2(image, dirImages())
        image = os.path.basename(image)

    items[code] = {
        'item': item,
        'cost': cost,
        'image': image
    }
    saveData()

# Elimina una fruta
def unsetFruit(code):
    global items
    if code in items:
        items.pop(code)
        saveData()
        return True
    return False

# Notificación de alerta
def notifyAlert(message, entry = None):
    notification('Alerta', message=message, app_name=appName(), timeout=1500)

    if not entry is None:
        entry.focus()

# Notificación de éxito
def notifySuccess(message):
    notification('Éxito', message=message, app_name=appName(), timeout=1500)

# Determina si existe el código de una fruta
def existsFruit(code) -> bool:
    global items
    return code in items

# Retorna el diccionario de frutas
def getFruits():
    global items
    return items

# Busca y retorna una fruta por código
def findFruit(code):
    global items
    return None if not code in items else items[code]

# Crea una imagen de tamaño determinado
def createIcon(code, width):
    global items

    if code is None or items[code]['image'] is None:
        return icon_to_image('expand', fill="#4267B2", scale_to_width=width-6)
    else:
        path = dirImages(items[code]['image'])
        image = Image.open(path)
        image.thumbnail((width, width))
        return ImageTk.PhotoImage(image)

from notifypy import Notify

# Obtiene el nombre de la aplicación
def appName() -> str:
    return 'Catálogo de vacantes de empresas'

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

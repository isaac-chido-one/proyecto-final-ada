import vacancies
from vacancies.structures.app import loadStructures, storeStructures

# Obtiene información desde un archivo json y la guarda en las estructuras correspondientes.
loadStructures(__file__)

# Ventana principal
app = vacancies.Menu()
app.mainloop()

# Guarda la información de las estructuras en un archivo json.
storeStructures()

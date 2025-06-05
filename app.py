import vacancies
from vacancies.structures.app import loadStructures, storeStructures

loadStructures(__file__)
app = vacancies.Menu()
app.mainloop()
storeStructures()

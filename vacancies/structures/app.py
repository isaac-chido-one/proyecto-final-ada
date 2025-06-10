import json, os
from typing import Any, Callable, Optional
from vacancies.entities.applicant import Applicant
from vacancies.entities.experience import Experience
from vacancies.entities.vacancy import Vacancy
from vacancies.structures.stack import Stack
from vacancies.structures.node import Node
from vacancies.utils import appendDictionaryToArray

# TODO: Renombrar como persistence.py

# Ruta del archivo json para guardar y leer la información de las estructuras.
filename = ''

# Pila global para guardar todas las vacantes.
listVacancies = None

# Pila global para guardar todos los candidatos.
stackApplicants = Stack()

def findApplicant(applicant: Applicant) -> Optional[Applicant]:
	''' Busca un candidato en la pila global de candidatos. '''
	global stackApplicants
	return stackApplicants.find(applicant)

def findVacancy(vacancy: Vacancy) -> Optional[Vacancy]:
	''' Busca una vacante en la lista global de vacantes. '''
	global listVacancies
	return Node.find(listVacancies, vacancy)

def forEachApplicant(callback: Callable[[Applicant, Any], None], args):
	''' Ejecuta una función por cada candidato de la pila global. '''
	global stackApplicants
	stackApplicants.each(callback, args)

def forEachVacancy(callback: Callable[[Vacancy, Any], None], args):
	''' Ejecuta una función por cada vacante de la lista global. '''
	global listVacancies
	Node.each(listVacancies, callback, args)

def insertApplicant(applicant: Applicant):
	''' Agrega un candidato a la pila global. '''
	global stackApplicants
	stackApplicants.Apilar(applicant)

def insertVacancy(vacancy: Vacancy):
	''' Agrega una vacante a la lista global. '''
	global listVacancies
	listVacancies = Node(vacancy, listVacancies)

def removeApplicant(applicant: Applicant):
	''' Quita un candidato de la pila global. '''
	global stackApplicants
	stackApplicants.remove(applicant)

def removeVacancy(vacancy: Vacancy):
	''' Quita una vacante de la lista global. '''
	global listVacancies
	listVacancies = Node.remove(listVacancies, vacancy)

def sortApplicants(field: str):
	'''
	Ordena la pila global de candidatos de menor a mayor por el atributo
	especificado con el algoritmo Insertion Sort.
	'''
	global stackApplicants
	stackApplicants.insertSort(field)

def sortVacancies(field: str):
	'''
	Ordena la lista global de vacantes de menor a mayor por el atributo
	especificado con el algoritmo Bubble Sort.
	'''
	Node.bubleSort(listVacancies, field)

def loadStructures(source_file: str):
	''' Obtiene información desde un archivo json y la guarda en las estructuras correspondientes. '''
	global filename
	directory = os.path.dirname(os.path.abspath(source_file)) + os.sep + 'storage'

	if not os.path.exists(directory):
		os.makedirs(directory)

	filename = directory + os.sep + 'vacancies.json'

	if not os.path.exists(filename):
		return

	with open(filename) as json_file:
		dictionary = json.load(json_file)

	for elem in dictionary['applicants']:
		applicant = Applicant.from_dictionary(elem)
		insertApplicant(applicant)

		if 'experience' in elem:
			for row in elem['experience']:
				experience = Experience.from_dictionary(row)
				hash = experience.hash()
				applicant.experience.set(hash, experience)

	for elem in dictionary['vacancies']:
		vacancy = Vacancy.from_dictionary(elem)
		insertVacancy(vacancy)

		if 'applicants' in elem:
			for row in elem['applicants']:
				first_name = row['first_name']
				last_name = row['last_name']
				applicantForFind = Applicant(first_name=first_name, last_name=last_name)
				applicant = findApplicant(applicantForFind)

				if applicant is not None:
					vacancy.applicants.Apilar(applicant)

def storeStructures():
	''' Guarda la información de las estructuras en un archivo json. '''
	global filename, stackApplicants, listVacancies
	applicants = []
	stackApplicants.each(appendDictionaryToArray, applicants)
	vacancies = []
	Node.each(listVacancies, appendDictionaryToArray, vacancies)
	dictionary = {
		'applicants': applicants,
		'vacancies': vacancies
	}
	js = json.dumps(dictionary)
	file = open(filename, 'w')
	file.write(js)
	file.close()

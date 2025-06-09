import json, os
from typing import Any, Callable, Optional
from vacancies.entities.applicant import Applicant
from vacancies.entities.vacancy import Vacancy
from vacancies.structures.stack import Stack
from vacancies.structures.node import Node

filename = ''
hashmapExperience = None
listVacancies = None
stackApplicants = Stack()

def findApplicant(applicant: Applicant) -> Optional[Applicant]:
	global stackApplicants
	return stackApplicants.find(applicant)

def findVacancy(vacancy: Vacancy) -> Optional[Vacancy]:
	global listVacancies
	return Node.find(listVacancies, vacancy)

def forEachApplicant(callback: Callable[[Applicant, Any], None], args):
	global stackApplicants
	stackApplicants.each(callback, args)

def forEachVacancy(callback: Callable[[Vacancy, Any], None], args):
	global listVacancies
	Node.each(listVacancies, callback, args)

def insertApplicant(applicant: Applicant):
	global stackApplicants
	stackApplicants.Apilar(applicant)

def insertVacancy(vacancy: Vacancy):
	global listVacancies
	listVacancies = Node(vacancy, listVacancies)

def removeApplicant(applicant: Applicant):
	global stackApplicants
	stackApplicants.remove(applicant)

def removeVacancy(vacancy: Vacancy):
	global listVacancies
	listVacancies = Node.remove(listVacancies, vacancy)

def sortApplicants(field: str):
	global stackApplicants
	stackApplicants.insertSort(field)

def sortVacancies(field: str):
	Node.bubleSort(listVacancies, field)

def loadStructures(source_file: str):
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

def to_dictionary(data, array):
	array.append(data.to_dictionary())

def storeStructures():
	global filename, stackApplicants, listVacancies
	applicants = []
	stackApplicants.each(to_dictionary, applicants)
	vacancies = []
	Node.each(listVacancies, to_dictionary, vacancies)
	dictionary = {
		'applicants': applicants,
		'experience': [],
		'vacancies': vacancies
	}
	js = json.dumps(dictionary)
	file = open(filename, 'w')
	file.write(js)
	file.close()

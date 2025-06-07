import json, os
from vacancies.entities.applicant import Applicant
from vacancies.entities.vacancy import Vacancy
from vacancies.structures.stack import Stack
from vacancies.structures.node import Node

filename = ''
hashmapExperience = None
listVacancies = None
stackApplicants = Stack()

def findApplicant(applicant):
	global stackApplicants
	return stackApplicants.find(applicant)

def findVacancy(vacancy):
	global listVacancies
	return Node.find(listVacancies, vacancy)

def forEachApplicant(callback, args):
	global stackApplicants
	stackApplicants.each(callback, args)

def forEachVacancy(callback, args):
	global listVacancies
	Node.each(listVacancies, callback, args)

def insertApplicant(applicant):
	global stackApplicants
	stackApplicants.Apilar(applicant)

def insertVacancy(vacancy):
	global listVacancies
	listVacancies = Node(vacancy, listVacancies)

def removeApplicant(applicant):
	global stackApplicants
	stackApplicants.remove(applicant)

def removeVacancy(vacancy):
	global listVacancies
	listVacancies = Node.remove(listVacancies, vacancy)

def loadStructures(source_file):
	global filename
	directory = os.path.dirname(os.path.abspath(source_file)) + os.sep + 'storage'

	if not os.path.exists(directory):
		os.makedirs(directory)

	filename = directory + os.sep + 'vacancies.json'

	if not os.path.exists(filename):
		return

	with open(filename) as json_file:
		dictionary = json.load(json_file)

	print(dictionary)

	for elem in dictionary['applicants']:
		applicant = Applicant.from_dictionary(elem)
		insertApplicant(applicant)

	for elem in dictionary['vacancies']:
		vacancy = Vacancy.from_dictionary(elem)
		insertVacancy(vacancy)

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

from vacancies.entities.experience import Experience
from vacancies.structures.hash_table import HashTable

class Applicant:

	def __init__(
			self,
			email: str = '',
			first_name: str = '',
			last_name: str = '',
			phone: str = '',
			resume: str = ''
	):
		self.__email = email
		self.__experience = HashTable()
		self.__first_name = first_name
		self.__last_name = last_name
		self.__phone = phone
		self.__resume = resume

	@property
	def email(self) -> str:
		return self.__email

	@property
	def experience(self) -> HashTable:
		return self.__experience

	@property
	def first_name(self) -> str:
		return self.__first_name

	@property
	def last_name(self) -> str:
		return self.__last_name

	@property
	def phone(self) -> str:
		return self.__phone

	@property
	def resume(self) -> str:
		return self.__resume

	@email.setter
	def email(self, email: str):
		self.__email = email

	@first_name.setter
	def first_name(self, first_name: str):
		self.__first_name = first_name

	@last_name.setter
	def last_name(self, last_name: str):
		self.__last_name = last_name

	@phone.setter
	def phone(self, phone: str):
		self.__phone = phone

	@resume.setter
	def resume(self, resume: str):
		self.__resume = resume

	def __eq__(self, other):
		return isinstance(other, Applicant) and self.__first_name == other.__first_name and self.__last_name == other.__last_name

	def __repr__(self):
		return '"{0} {1}"'.format(self.__first_name, self.__last_name)

	def compare(self, other, attribute_name) -> int:
		a = getattr(self, attribute_name)
		b = getattr(other, attribute_name)
		a = a.lower()
		b = b.lower()

		return 0 if a == b else (-1 if a < b else 1)

	def buildExperienceArray(self, experience: Experience, array):
		array.append(experience.to_dictionary())

	def to_dictionary(self) -> dict:
		experience = []
		self.experience.each(self.buildExperienceArray, experience)

		return {
			'email': self.__email,
			'experience': experience,
			'first_name': self.__first_name,
			'last_name': self.__last_name,
			'phone': self.__phone,
			'resume': self.__resume
		}

	@staticmethod
	def from_dictionary(dictionary: dict):
		email = dictionary['email']
		first_name = dictionary['first_name']
		last_name = dictionary['last_name']
		phone = dictionary['phone']
		resume = dictionary['resume']

		return Applicant(email, first_name, last_name, phone, resume)

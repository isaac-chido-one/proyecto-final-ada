from vacancies.utils import appendDictionaryToArray
from vacancies.entities.experience import Experience
from vacancies.structures.hash_table import HashTable

class Applicant:
	'''
	Clase candidato

	Attributes:
		email (str): Correo.
		experience (HashTable): Tabla hash para guardar la experiencia de este candidato.
		first_name (str): Nombres.
		last_name (str): Apellidos.
		phone (str): Teléfono.
		resume (str): Currículum.
	'''

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
		''' Correo '''
		return self.__email

	@property
	def experience(self) -> HashTable:
		''' Tabla hash de experiencia '''
		return self.__experience

	@property
	def first_name(self) -> str:
		''' Nombres '''
		return self.__first_name

	@property
	def last_name(self) -> str:
		''' Apellidos '''
		return self.__last_name

	@property
	def phone(self) -> str:
		''' Teléfono '''
		return self.__phone

	@property
	def resume(self) -> str:
		''' Currículum '''
		return self.__resume

	@email.setter
	def email(self, email: str):
		''' Correo '''
		self.__email = email

	@first_name.setter
	def first_name(self, first_name: str):
		''' Nombres '''
		self.__first_name = first_name

	@last_name.setter
	def last_name(self, last_name: str):
		''' Apellidos '''
		self.__last_name = last_name

	@phone.setter
	def phone(self, phone: str):
		''' Teléfono '''
		self.__phone = phone

	@resume.setter
	def resume(self, resume: str):
		''' Currículum '''
		self.__resume = resume

	def __eq__(self, other):
		return isinstance(other, Applicant) and self.__first_name == other.__first_name and self.__last_name == other.__last_name

	def __repr__(self):
		return '"{0} {1}"'.format(self.__first_name, self.__last_name)

	def compare(self, other, attribute_name: str) -> int:
		''' Función comparadora por atributo de esta clase. '''
		a = getattr(self, attribute_name)
		b = getattr(other, attribute_name)
		a = a.lower()
		b = b.lower()

		return 0 if a == b else (-1 if a < b else 1)

	def to_dictionary(self) -> dict:
		''' Convierte una instancia a diccionario. Para guardar en archivo json. '''
		experience = []
		self.experience.each(appendDictionaryToArray, experience)

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
		''' Convierte un diccionario a una instancia de esta clase. Para leer desde archivo json. '''
		email = dictionary['email']
		first_name = dictionary['first_name']
		last_name = dictionary['last_name']
		phone = dictionary['phone']
		resume = dictionary['resume']

		return Applicant(email, first_name, last_name, phone, resume)


class Applicant:

	def __init__(self, email = '', first_name = '', last_name = '', phone = '', resume = ''):
		self.__email = email
		self.__first_name = first_name
		self.__last_name = last_name
		self.__phone = phone
		self.__resume = resume

	@property
	def email(self):
		return self.__email

	@property
	def first_name(self):
		return self.__first_name

	@property
	def last_name(self):
		return self.__last_name

	@property
	def phone(self):
		return self.__phone

	@property
	def resume(self):
		return self.__resume

	@email.setter
	def email(self, email):
		self.__email = email

	@first_name.setter
	def first_name(self, first_name):
		self.__first_name = first_name

	@last_name.setter
	def last_name(self, last_name):
		self.__last_name = last_name

	@phone.setter
	def phone(self, phone):
		self.__phone = phone

	@resume.setter
	def resume(self, resume):
		self.__resume = resume

	def __eq__(self, other):
		return isinstance(other, Applicant) and self.__first_name == other.__first_name and self.__last_name == other.__last_name

	def __repr__(self):
		return '{0};{1}'.format(self.__first_name, self.__last_name)

	def to_dictionary(self):
		return {
			'email': self.__email,
			'first_name': self.__first_name,
			'last_name': self.__last_name,
			'phone': self.__phone,
			'resume': self.__resume
		}

	@staticmethod
	def from_dictionary(dictionary):
		email = dictionary['email']
		first_name = dictionary['first_name']
		last_name = dictionary['last_name']
		phone = dictionary['phone']
		resume = dictionary['resume']
		return Applicant(email, first_name, last_name, phone, resume)


class Applicant:

	def __init__(self, email = '', first_name = '', last_name = '', phone = '', resume = '', vacancy = None):
		self.__email = email
		self.__first_name = first_name
		self.__last_name = last_name
		self.__phone = phone
		self.__resume = resume
		self.__vacancy = vacancy

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

	@property
	def vacancy(self):
		return self.__vacancy

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

	@vacancy.setter
	def vacancy(self, vacancy):
		self.__vacancy = vacancy

	def __repr__(self):
		return 'Nombres: {0} Apellidos: {1}'.format(self.__first_name, self.__last_name)

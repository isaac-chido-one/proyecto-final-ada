from slugify import slugify

class Vacancy:

	def __init__(self, company = '', description = '', location = '', max_salary = None, min_salary = None, requirements = '', title = ''):
		self.__company = company
		self.__description = description
		self.__location = location
		self.__max_salary = max_salary
		self.__min_salary = min_salary
		self.__requirements = requirements
		self.__title = title

	@property
	def company(self):
		return self.__company

	@property
	def description(self):
		return self.__description

	@property
	def location(self):
		return self.__location

	@property
	def max_salary(self):
		return self.__max_salary

	@property
	def min_salary(self):
		return self.__min_salary

	@property
	def requirements(self):
		return self.__requirements

	@property
	def title(self):
		return self.__title

	@company.setter
	def company(self, company):
		self.__company = company

	@description.setter
	def description(self, description):
		self.__description = description

	@location.setter
	def location(self, location):
		self.__location = location

	@max_salary.setter
	def max_salary(self, max_salary):
		self.__max_salary = max_salary

	@min_salary.setter
	def min_salary(self, min_salary):
		self.__min_salary = min_salary

	@requirements.setter
	def requirements(self, requirements):
		self.__requirements = requirements

	@title.setter
	def title(self, title):
		self.__title = title

	def __eq__(self, other):
		return isinstance(other, Vacancy) and self.__company == other.__company and self.__title == other.__title and self.__location == other.__location

	def __repr__(self):
		return '{0};{1};{2}'.format(
			slugify(self.__company),
			slugify(self.__title),
			slugify(self.__location)
		)

	def to_dictionary(self):
		return {
			'company': self.__company,
			'description': self.__description,
			'location': self.__location,
			'max_salary': self.__max_salary,
			'min_salary': self.__min_salary,
			'requirements': self.__requirements,
			'title': self.__title
		}

	@staticmethod
	def from_dictionary(dictionary):
		company = dictionary['company']
		description = dictionary['description']
		location = dictionary['location']
		max_salary = dictionary['max_salary']
		min_salary = dictionary['min_salary']
		requirements = dictionary['requirements']
		title = dictionary['title']
		return Vacancy(company, description, location, max_salary, min_salary, requirements, title)

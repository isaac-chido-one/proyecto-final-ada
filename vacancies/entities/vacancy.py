
class Vacancy:

	def __init__(self, company = '', description = '', location = '', max_salary = 0, min_salary = 0, requirements = '', title = ''):
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

	def __repr__(self):
		return 'Puesto: {0} Empresa: {1}'.format(self.__title, self.__company)

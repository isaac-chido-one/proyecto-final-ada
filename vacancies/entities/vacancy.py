from typing import Optional

class Vacancy:

	def __init__(
			self,
			company: str = '',
			description: str = '',
			location: str = '',
			max_salary:Optional[float] = None,
			min_salary:Optional[float] = None,
			requirements: str = '',
			title: str = ''
	):
		self.__company = company
		self.__description = description
		self.__location = location
		self.__max_salary = max_salary
		self.__min_salary = min_salary
		self.__requirements = requirements
		self.__title = title

	@property
	def company(self) -> str:
		return self.__company

	@property
	def description(self) -> str:
		return self.__description

	@property
	def location(self) -> str:
		return self.__location

	@property
	def max_salary(self) -> Optional[float]:
		return self.__max_salary

	@property
	def min_salary(self) -> Optional[float]:
		return self.__min_salary

	@property
	def requirements(self) -> str:
		return self.__requirements

	@property
	def title(self) -> str:
		return self.__title

	@company.setter
	def company(self, company: str):
		self.__company = company

	@description.setter
	def description(self, description: str):
		self.__description = description

	@location.setter
	def location(self, location: str):
		self.__location = location

	@max_salary.setter
	def max_salary(self, max_salary: Optional[float]):
		self.__max_salary = max_salary

	@min_salary.setter
	def min_salary(self, min_salary: Optional[float]):
		self.__min_salary = min_salary

	@requirements.setter
	def requirements(self, requirements: str):
		self.__requirements = requirements

	@title.setter
	def title(self, title: str):
		self.__title = title

	def __eq__(self, other):
		return isinstance(other, Vacancy) and self.__company == other.__company and self.__title == other.__title and self.__location == other.__location

	def __repr__(self):
		return '"{0}"'.format(self.__title)

	def compare(self, other, attribute_name) -> int:
		a = getattr(self, attribute_name)
		b = getattr(other, attribute_name)

		if a is None and b is None:
			return 0
		elif a is None:
			return -1
		elif b is None:
			return 1

		if attribute_name != 'max_salary' and attribute_name != 'min_salary':
			a = a.lower()
			b = b.lower()

		return 0 if a == b else (-1 if a < b else 1)

	def to_dictionary(self) -> dict:
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
	def from_dictionary(dictionary: dict):
		company = dictionary['company']
		description = dictionary['description']
		location = dictionary['location']
		max_salary = dictionary['max_salary']
		min_salary = dictionary['min_salary']
		requirements = dictionary['requirements']
		title = dictionary['title']
		return Vacancy(company, description, location, max_salary, min_salary, requirements, title)

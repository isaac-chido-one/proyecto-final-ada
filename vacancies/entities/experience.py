from typing import Optional
from vacancies.entities.applicant import Applicant

class Experience:

	def __init__(
			self,
			applicant:Applicant,
			ending_year:Optional[int] = None,
			institution: str = '',
			starting_year:Optional[int] = None,
			title: str = '',
			type: int = 0
	):
		self.__applicant = applicant
		self.__ending_year = ending_year
		self.__institution = institution
		self.__starting_year = starting_year
		self.__title = title
		self.__type = type

	@property
	def applicant(self) -> Applicant:
		return self.__applicant

	@property
	def ending_year(self) -> Optional[int]:
		return self.__ending_year

	@property
	def institution(self) -> str:
		return self.__institution

	@property
	def starting_year(self) -> Optional[int]:
		return self.__starting_year

	@property
	def title(self) -> str:
		return self.__title

	@property
	def type(self):
		return self.__type

	@applicant.setter
	def applicant(self, applicant: Applicant):
		self.__applicant = applicant

	@ending_year.setter
	def ending_year(self, ending_year: Optional[int]):
		self.__ending_year = ending_year

	@institution.setter
	def institution(self, institution: str):
		self.__institution = institution

	@starting_year.setter
	def starting_year(self, starting_year: Optional[int]):
		self.__starting_year = starting_year

	@title.setter
	def title(self, title: str):
		self.__title = title

	@type.setter
	def type(self, type: int):
		self.__type = type

	def __repr__(self):
		return 'Puesto o estudio: {0} Empresa o institucion: {1}'.format(self.__title, self.__institution)

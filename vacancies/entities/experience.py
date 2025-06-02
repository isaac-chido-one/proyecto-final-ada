
class Experience:

	def __init__(self, applicant = None, ending_year = 2025, institution = '', starting_year = 2025, title = '', type = 0):
		self.__applicant = applicant
		self.__ending_year = ending_year
		self.__institution = institution
		self.__starting_year = starting_year
		self.__title = title
		self.__type = type

	@property
	def applicant(self):
		return self.__applicant

	@property
	def ending_year(self):
		return self.__ending_year

	@property
	def institution(self):
		return self.__institution

	@property
	def starting_year(self):
		return self.__starting_year

	@property
	def title(self):
		return self.__title

	@property
	def type(self):
		return self.__type

	@applicant.setter
	def applicant(self, applicant):
		self.__applicant = applicant

	@ending_year.setter
	def ending_year(self, ending_year):
		self.__ending_year = ending_year

	@institution.setter
	def institution(self, institution):
		self.__institution = institution

	@starting_year.setter
	def starting_year(self, starting_year):
		self.__starting_year = starting_year

	@title.setter
	def title(self, title):
		self.__title = title

	@type.setter
	def type(self, type):
		self.__type = type

	def __repr__(self):
		return 'Puesto o estudio: {0} Empresa o institucion: {1}'.format(self.__title, self.__institution)

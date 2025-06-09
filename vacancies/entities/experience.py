from slugify import slugify
from typing import Final, Optional

class Experience:
	TYPES: Final = [
		'Estudio o grado',
		'Puesto anterior',
		'Curso',
		'Certificación',
	]

	def __init__(
			self,
			ending_year:Optional[int] = None,
			institution: str = '',
			starting_year:Optional[int] = None,
			title: str = '',
			type: int = 0
	):
		self.__ending_year = ending_year
		self.__institution = institution
		self.__starting_year = starting_year
		self.__title = title
		self.__type = type

	@property
	def ending_year(self) -> Optional[int]:
		return self.__ending_year

	@property
	def institution(self) -> str:
		return self.__institution

	@property
	def repr_type(self):
		return self.TYPES[self.__type]

	@property
	def starting_year(self) -> Optional[int]:
		return self.__starting_year

	@property
	def title(self) -> str:
		return self.__title

	@property
	def type(self):
		return self.__type

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

	def hash(self) -> str:
		return '{0};{1};{2}'.format(self.__type, slugify(self.__title), slugify(self.__institution))

	def __repr__(self):
		return '"{0} - {1} - {2}"'.format(self.repr_type, self.__title, self.__institution)

	def to_dictionary(self) -> dict:
		return {
			'ending_year': self.__ending_year,
			'institution': self.__institution,
			'starting_year': self.__starting_year,
			'title': self.__title,
			'type': self.__type
		}

	@staticmethod
	def from_dictionary(dictionary: dict):
		ending_year = dictionary['ending_year']
		institution = dictionary['institution']
		starting_year = dictionary['starting_year']
		title = dictionary['title']
		type = dictionary['type']

		return Experience(ending_year=ending_year, institution=institution, starting_year=starting_year, title=title, type=type)

	def compare(self, other, attribute_name: str) -> int:
		a = getattr(self, attribute_name)
		b = getattr(other, attribute_name)

		if a is None and b is None:
			return 0
		elif a is None:
			return -1
		elif b is None:
			return 1

		if attribute_name != 'ending_year' and attribute_name != 'starting_year':
			a = a.lower()
			b = b.lower()

		return 0 if a == b else (-1 if a < b else 1)

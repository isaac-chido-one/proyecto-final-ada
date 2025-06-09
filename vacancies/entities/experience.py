from slugify import slugify
from typing import Final, Optional

class Experience:
	'''
	Clase experiencia

	Attributes:
		ending_year (int | None): Año final del registro de experiencia.
		institution (str): Empresa anterior, escuela, universidad o institución.
		starting_year (int | None): Año inicial del registro de experiencia.
		title (str): Puesto anterior, estudio, nombre del taller o curso.
		type (int): Tipo de experiencia.
	'''

	TYPES: Final = [
		'Estudio o grado',
		'Puesto anterior',
		'Curso',
		'Certificación',
		'Taller',
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
		''' Año final del registro de experiencia '''
		return self.__ending_year

	@property
	def institution(self) -> str:
		''' Empresa anterior, escuela, universidad o institución '''
		return self.__institution

	@property
	def repr_type(self):
		''' Tipo de experiencia mapeado en cadena de texto '''
		return self.TYPES[self.__type]

	@property
	def starting_year(self) -> Optional[int]:
		''' Año inicial del registro de experiencia '''
		return self.__starting_year

	@property
	def title(self) -> str:
		''' Puesto anterior, estudio, nombre del taller o curso '''
		return self.__title

	@property
	def type(self):
		''' Tipo de experiencia '''
		return self.__type

	@ending_year.setter
	def ending_year(self, ending_year: Optional[int]):
		''' Año final del registro de experiencia '''
		self.__ending_year = ending_year

	@institution.setter
	def institution(self, institution: str):
		''' Empresa anterior, escuela, universidad o institución '''
		self.__institution = institution

	@starting_year.setter
	def starting_year(self, starting_year: Optional[int]):
		''' Año inicial del registro de experiencia '''
		self.__starting_year = starting_year

	@title.setter
	def title(self, title: str):
		''' Puesto anterior, estudio, nombre del taller o curso '''
		self.__title = title

	@type.setter
	def type(self, type: int):
		''' Tipo de experiencia '''
		self.__type = type

	def hash(self) -> str:
		''' Arma la llave hash '''
		return '{0};{1};{2}'.format(self.__type, slugify(self.__title), slugify(self.__institution))

	def __repr__(self):
		return '"{0} - {1} - {2}"'.format(self.repr_type, self.__title, self.__institution)

	def to_dictionary(self) -> dict:
		''' Convierte una instancia a diccionario. Para guardar en archivo json. '''
		return {
			'ending_year': self.__ending_year,
			'institution': self.__institution,
			'starting_year': self.__starting_year,
			'title': self.__title,
			'type': self.__type
		}

	@staticmethod
	def from_dictionary(dictionary: dict):
		''' Convierte un diccionario a una instancia de esta clase. Para leer desde archivo json. '''
		ending_year = dictionary['ending_year']
		institution = dictionary['institution']
		starting_year = dictionary['starting_year']
		title = dictionary['title']
		type = dictionary['type']

		return Experience(ending_year=ending_year, institution=institution, starting_year=starting_year, title=title, type=type)

	def compare(self, other, attribute_name: str) -> int:
		''' Función comparadora por atributo de esta clase. '''
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

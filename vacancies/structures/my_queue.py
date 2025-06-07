from typing import Any
from node import Node

class Queue():
	''' Clase cola '''

	def __init__(self):
		self.Inicializar()

	def Cima(self):
		''' Mostrar el siguiente elemento que se sacaría (sin sacarlo). '''
		return None if self.Vacia() else self.__header.data # type: ignore

	def Contiene(self, element: Any) -> bool:
		''' Comprobar si un elemento está en la estructura. '''
		return Node.contains(self.__header, element)

	def Desencolar(self) -> Any:
		if self.Vacia():
			return None

		node = self.__header
		self.__header = self.__header.link # type: ignore
		node.link = None # type: ignore

		if self.__header is None:
			self.__last = None

		return node.data # type: ignore

	def Encolar(self, element: Any):
		node = Node(element, None)

		if self.Vacia():
			self.__header = node
		else:
			self.__last.link = node # type: ignore

		self.__last = node

	def Inicializar(self):
		self.__header = None
		self.__last = None

	def Limpiar(self):
		self.Inicializar()

	def Mostrar(self):
		''' Mostrar el contenido de la estructura. '''
		Node.print(self.__header)

	def Primero(self) -> Any:
		node = Node.first(self.__header)
		return None if node is None else node.data

	def Tamano(self) -> int:
		''' Contar el número de elementos. '''
		return Node.length(self.__header)

	def Vacia(self) -> bool:
		return self.__header is None and self.__last is None

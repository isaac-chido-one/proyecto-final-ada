from typing import Any, Callable
from vacancies.structures.node import Node

class Stack():
	''' Clase pila '''

	def __init__(self):
		self.Inicializar()

	def Apilar(self, element: Any):
		''' Insertar un elemento. '''
		self.__node = Node(element, self.__node)
		return True

	def Cima(self) -> Any:
		''' Mostrar el siguiente elemento que se sacaría (sin sacarlo). '''
		return None if self.Vacia() else self.__node.data # type: ignore

	def Contiene(self, element: Any) -> bool:
		''' Comprobar si un elemento está en la estructura. '''
		return Node.contains(self.__node, element)

	def Desapilar(self) -> Any:
		''' Sacar un elemento. '''
		if self.Vacia():
			return None
		element = self.__node.data # type: ignore
		self.__node = self.__node.link # type: ignore

		return element

	def Inicializar(self):
		self.__node = None

	def Limpiar(self):
		self.Inicializar()

	def Mostrar(self):
		''' Mostrar el contenido de la estructura. '''
		Node.print(self.__node)

	def Primero(self) -> Any:
		node = Node.first(self.__node)
		return None if node is None else node.data

	def Tamano(self) -> int:
		''' Contar el número de elementos. '''
		return Node.length(self.__node)

	def Vacia(self) -> bool:
		return self.__node is None

	def each(self, callback: Callable[[Any, Any], None], args: Any):
		''' Ejecuta una funcion en cada elemento de cada nodo. '''
		Node.each(self.__node, callback, args)

	def find(self, element: Any) -> Any:
		''' Busca un elemento por comparación y regresa el elemento encontrado '''
		return Node.find(self.__node, element)

	def remove(self, element: Any):
		self.__node = Node.remove(self.__node, element)
